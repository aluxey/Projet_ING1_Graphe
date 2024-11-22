// Initialize the map
const map = L.map("map", {
  crs: L.CRS.Simple,
  maxZoom: 2,
});

const bounds = [
  [0, 0],
  [1000, 1000],
];

// Add the map image
L.imageOverlay("../Data/Data/metrof_r.png", bounds).addTo(map);
map.fitBounds(bounds);

// Function to load and display stations from JSON
async function loadStations() {
  try {
    // Fetch the JSON file
    const response = await fetch("/Server/pospoints.json");
    if (!response.ok) {
      throw new Error("Failed to load stations data");
    }
    const data = await response.json();

    // Create markers for each station
    data.positions.forEach((station) => {
      // Convert the coordinates to the format Leaflet expects  
      const coords = [1000 - station.posY, station.posX]; 

      // Create custom icon for the station
      const stationIcon = L.divIcon({
        className: "station-marker",
        html: "●", 
        iconSize: [10, 10],
        iconAnchor: [5, 5],
      });

      // Create the marker with a popup
      L.marker(coords, { icon: stationIcon }).addTo(map).bindPopup(`
                    <strong>${station.nom_station.replace(
                      "@",
                      " "
                    )}</strong><br>
                    Position: ${station.posX}, ${station.posY}
                `);
    });
  } catch (error) {
    console.error("Error loading stations:", error);
  }
}

const style = document.createElement("style");
style.textContent = `
    .station-marker {
        color: #e74c3c;
        font-size: 14px;
        text-align: center;
        line-height: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .leaflet-popup-content {
        margin: 10px;
    }
    
    .leaflet-popup-content strong {
        color: #2c3e50;
    }
`;
document.head.appendChild(style);

loadStations();
