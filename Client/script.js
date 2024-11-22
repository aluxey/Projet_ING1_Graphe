const map = L.map("map", {
  crs: L.CRS.Simple,
  maxZoom: 2,
  minZoom: -2,
  backgroundColor: "#f8f9fa",
});

const bounds = [
  [0, 0],
  [1000, 1000],
];

map.fitBounds(bounds);

const lineColors = {
  1: "#FFCD00", // Yellow
  2: "#003CA6", // Dark Blue
  3: "#837902", // Olive
  4: "#CF009E", // Magenta
  5: "#FF7E2E", // Orange
  6: "#6ECA97", // Light Green
  7: "#FA9ABA", // Pink
  8: "#E19BDF", // Lilac
  9: "#B6BD00", // Chartreuse
  10: "#C9910D", // Golden
  11: "#704B1C", // Brown
  12: "#007852", // Green
  13: "#6EC4E8", // Light Blue
  14: "#62259D", // Purple
};


async function loadStationPositions() {
  try {
    const response = await fetch("/Server/pospoints.json");
    if (!response.ok) throw new Error("Failed to load positions data"); // on recupere les données du json que l'on a créé et on s'assure qu'on le recupere bien
    const positionsData = await response.json();
    return Object.fromEntries(
      positionsData.positions.map((pos) => [
        pos.nom_station.replace("@", " ").trim(), // on clean les nom de certaines stations qui avait des signes dans leur nom
        pos,
      ])
    );
  } catch (error) {
    console.error("Error loading station positions:", error);
  }
}


async function loadMetroData() {
  try {
    const response = await fetch("/Server/sorted_metro.json");
    if (!response.ok) throw new Error("Failed to load metro data"); // on recupere les données du json que l'on a créé et on s'assure qu'on le recupere bien
    const metroData = await response.json();
    return metroData;
  } catch (error) {
    console.error("Error loading metro data:", error);
  }
}

function createStationMarker(station, position, positionsMap) {
  const coords = [1000 - position.posY, position.posX]; // Position de la station positionnée sur la map
  const isTerminus = station.terminus === "True"; 

  const stationIcon = L.divIcon({
    className: `station-marker ${isTerminus ? "terminus-marker" : ""}`,
    html: isTerminus ? "★" : "●", // si on a un terminus alors on met une émote en place en forme d'étoile sinon on garde le point classsique
    iconSize: [15, 15],
    iconAnchor: [7.5, 7.5],
  });

  L.marker(coords, { icon: stationIcon })
    .addTo(map)
    .bindPopup(
      `
      <div>
        <strong>${station.name}</strong><br>
        <span style="color:${lineColors[station.ligne] || "#000"}">
          Line: ${station.ligne}
        </span><br>
        Terminus: ${isTerminus ? "Yes" : "No"}<br>
        Position: ${position.posX}, ${position.posY}
      </div>
    `
    )
    .on("mouseover", (e) => e.target.openPopup()) // au survol on affiche les informations sur la station
    .on("mouseout", (e) => e.target.closePopup());
}

function createMetroLine(startStation, endStation, positionsMap) {
  const startPos = positionsMap[startStation.name]; // on recupere la position de la station de départ
  const endPos = positionsMap[endStation.name]; // on recupere la position de la station d'arrivée

  if (startPos && endPos) {
    // On crée une ligne entre les deux points pour relier les stations
    const lineCoords = [
      [1000 - startPos.posY, startPos.posX],
      [1000 - endPos.posY, endPos.posX],
    ];

    // On ajoute la ligne sur la map
    L.polyline(lineCoords, {
      color: lineColors[startStation.ligne] || "#000000",
      weight: 4,
      opacity: 0.8,
      className: "metro-line",
    })
      .addTo(map)
      .bindTooltip(`Line ${startStation.ligne}`, {
        permanent: false,
        direction: "center",
        className: "line-tooltip",
      });
  }
}

async function loadStationsAndLines() {
  // On charge les stations et les lignes pour les afficher sur la map
  const positionsMap = await loadStationPositions();
  const metroData = await loadMetroData();

  // Add station markers to the map 
  metroData.stations.forEach((station) => {
    const stationName = station.name.trim();
    const position = positionsMap[stationName];

    if (position) {
      createStationMarker(station, position, positionsMap);
    } else {
      console.warn(`Position missing for station: ${stationName}`);
    }
  });

  // Add metro lines to the map
  metroData.edges.forEach((edge) => {
    const startStation = metroData.stations.find(
      (station) => station.id === edge.start
    );
    const endStation = metroData.stations.find(
      (station) => station.id === edge.end
    );

    if (startStation && endStation) {
      createMetroLine(startStation, endStation, positionsMap);
    }
  });
}

loadStationsAndLines();


// Add custom styles
const style = document.createElement("style");
style.textContent = `
    .station-marker {
        color: #e74c3c;
        font-size: 14px;
        text-align: center;
        line-height: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .terminus-marker {
        color: #2ecc71;
        font-size: 16px;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.5);
    }
    
    .leaflet-popup-content {
        margin: 10px;
    }
    
    .leaflet-popup-content strong {
        color: #2c3e50;
    }
    
    .metro-line {
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    
    .line-tooltip {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 4px;
        padding: 5px;
        font-weight: bold;
        color: #333;
    }
    
    .leaflet-container {
        border: 2px solid #2c3e50;
        border-radius: 10px;
    }
`;
document.head.appendChild(style);
