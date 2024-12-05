const colorLine = {
  1: "#FFCD00",
  2: "#003CA6",
  3: "#837902",
  3_1: "#6EC4E8",
  4: "#CF009E",
  5: "#FF7E2E",
  6: "#6ECA97",
  7: "#FA9ABA",
  7_1: "#6CAEDF",
  8: "#E19BDF",
  9: "#B6BD00",
  10: "#C9910D",
  11: "#704B1C",
  12: "#007852",
  13: "#6EC4E8",
  14: "#62259D",
};

async function loadMetroData() {
  const response = await fetch("/Server/Data/merged_data.json"); // Path to your JSON file
  return await response.json();
}

function buildElements(data) {
  const nodes = data.stations.map((station) => ({
    data: {
      id: `station-${station.id}`,
      name: station.name,
      ligne: station.ligne,
      terminus: station.terminus,
    },
    position: {
      x: station.posX || Math.random() * 1000, // Random position if missing
      y: station.posY || Math.random() * 1000,
    },
  }));

  const edges = data.edges.map((edge) => ({
    data: {
      id: `edge-${edge.start}-${edge.end}`,
      source: `station-${edge.start}`,
      target: `station-${edge.end}`,
      time: edge.time,
      ligne: data.stations.find((s) => s.id === edge.start)?.ligne || null,
    },
  }));

  return [...nodes, ...edges];
}

async function initCytoscape() {
  const data = await loadMetroData();
  const elements = buildElements(data);

  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: elements,
    style: [
      {
        selector: "node",
        style: {
          "background-color": "#fff", // Fond blanc
          "border-color": (ele) => colorLine[ele.data("ligne")] || "#000", // Bordure colorée selon la ligne
          "border-width": "2px",
          width: "8px",
          height: "8px",
          shape: "ellipse", // Forme circulaire
        },
      },
      // Style pour les terminus
      {
        selector: "node[terminus = 'True']", // Sélecteur pour les terminus
        style: {
          "background-color": "#fff", // Fond blanc
          "border-color": (ele) => colorLine[ele.data("ligne")] || "#000", // Bordure colorée selon la ligne
          "border-width": "4px", // Bordure plus épaisse pour les terminus
          width: "12px", // Nœud plus grand
          height: "12px", // Nœud plus grand
          shape: "rectangle", // Forme rectangulaire pour les terminus
        },
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": (ele) => colorLine[ele.data("ligne")] || "#ccc", // Couleur des lignes
          "curve-style": "bezier",
          "font-size": "6px",
          "font-weight": "bold",
          
        },
      },
    ],
    layout: {
      name: "preset", // Use preset positions from JSON
    },
  });

  // Add dynamic tooltips for nodes
  const tooltip = document.getElementById("tooltip");

  cy.on("mouseover", "node", (event) => {
    const node = event.target;
    tooltip.style.display = "block";
    tooltip.innerHTML = `
      <strong>${node.data("name")}</strong><br>
      Ligne: ${node.data("ligne")}<br>
      Terminus: ${node.data("terminus") === "True" ? "Oui" : "Non"}
    `;
  });

  cy.on("mouseout", "node", () => {
    tooltip.style.display = "none";
  });

  cy.on("mousemove", (event) => {
    tooltip.style.left = `${event.originalEvent.pageX + 10}px`;
    tooltip.style.top = `${event.originalEvent.pageY + 10}px`;
  });
}

initCytoscape();
