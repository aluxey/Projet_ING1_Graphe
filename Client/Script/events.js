import { cy } from "./cytoscapeInit.js";

let firstSelectedNode = null;
let secondSelectedNode = null;

let departureStation = null;
let destinationStation = null;
let parcoursButton = null;
let kruskalButton = null;

document.addEventListener("DOMContentLoaded", () => {
  // Initialize DOM elements
  departureStation = document.getElementById("depart");
  destinationStation = document.getElementById("arrive");
  parcoursButton = document.getElementById("parcoursButton");
  kruskalButton = document.getElementById("kruskalButton");

  if (!departureStation || !destinationStation || !parcoursButton) {
    console.error("Required DOM elements not found!");
    return;
  }

  // Attach event to the parcours button
  parcoursButton.addEventListener("click", parcours);
  kruskalButton.addEventListener("click", kruskal);
});

/**
 * Add Cytoscape event listeners.
 * @param {Object} cy - Cytoscape instance.
 */
export function addCytoscapeEvents(cy) {
  const tooltip = document.getElementById("tooltip");

  if (!cy || typeof cy.on !== "function") {
    console.error("Invalid Cytoscape instance provided.");
    return;
  }

  // Cytoscape events
  cy.on("mouseover", "node", (event) => showTooltip(event.target, tooltip));
  cy.on("mouseout", "node", () => hideTooltip(tooltip));
  cy.on("mousemove", (event) => moveTooltip(event, tooltip));
  cy.on("click", "node", (event) => handleNodeClick(event.target));

  cy.on("tap", (event) => {
    if (event.target === cy) {
      cy.elements().removeClass("highlighted"); // Clear highlights
      console.log("Graph reset to default state.");
    }
  });
}

/**
 * Show tooltip on node hover.
 * @param {Object} node - The hovered node.
 * @param {HTMLElement} tooltip - Tooltip element.
 */
function showTooltip(node, tooltip) {
  tooltip.style.display = "block";
  tooltip.innerHTML = `
    <strong>${node.data("name")}</strong><br>
    Ligne: ${node.data("ligne")}<br>
    Terminus: ${node.data("terminus") === "True" ? "Oui" : "Non"}
  `;
}

/**
 * Hide the tooltip.
 * @param {HTMLElement} tooltip - Tooltip element.
 */
function hideTooltip(tooltip) {
  tooltip.style.display = "none";
}

/**
 * Move the tooltip based on mouse position.
 * @param {Object} event - Mouse event.
 * @param {HTMLElement} tooltip - Tooltip element.
 */
function moveTooltip(event, tooltip) {
  tooltip.style.left = `${event.originalEvent.pageX + 10}px`;
  tooltip.style.top = `${event.originalEvent.pageY + 10}px`;
}

/**
 * Handle node click for selection.
 * @param {Object} node - The clicked node.
 */
function handleNodeClick(node) {
  if (!firstSelectedNode) {
    selectFirstNode(node);
  } else if (!secondSelectedNode && node !== firstSelectedNode) {
    selectSecondNode(node);
  } else {
    resetAndSelectFirstNode(node);
  }
}

/**
 * Select the first node (departure station).
 * @param {Object} node - Node to select as departure.
 */
function selectFirstNode(node) {
  firstSelectedNode = node;
  firstSelectedNode.data("depart", "True");
  firstSelectedNode.data("destination", "False");

  if (departureStation) {
    departureStation.innerHTML = `${firstSelectedNode.data(
      "name"
    )} ( Line ${firstSelectedNode.data("ligne")} )`;
  }
}

/**
 * Select the second node (destination station).
 * @param {Object} node - Node to select as destination.
 */
function selectSecondNode(node) {
  secondSelectedNode = node;
  secondSelectedNode.data("destination", "True");
  secondSelectedNode.data("depart", "False");

  if (destinationStation) {
    destinationStation.innerHTML = `${secondSelectedNode.data(
      "name"
    )} ( Line ${secondSelectedNode.data("ligne")} )`;
  }
}

/**
 * Reset selections and select a new departure station.
 * @param {Object} node - Node to reset and select as departure.
 */
function resetAndSelectFirstNode(node) {
  if (firstSelectedNode) {
    firstSelectedNode.data("depart", "False");
    firstSelectedNode.data("destination", "False");
  }

  if (secondSelectedNode) {
    secondSelectedNode.data("destination", "False");
    secondSelectedNode.data("depart", "False");
  }

  firstSelectedNode = node;
  secondSelectedNode = null;

  firstSelectedNode.data("depart", "True");
  firstSelectedNode.data("destination", "False");

  if (departureStation) {
    departureStation.innerHTML = `${firstSelectedNode.data(
      "name"
    )} ( Line ${firstSelectedNode.data("ligne")} )`;
  }

  if (destinationStation) {
    destinationStation.innerHTML = ""; // Clear destination display
  }

  alert(`Départ sélectionné: ${firstSelectedNode.data("name")}`);
}

/**
 * Handle the "Show Parcours" button click.
 */
async function parcours() {
  if (firstSelectedNode && secondSelectedNode) {
    const depart = firstSelectedNode.data("id").split("-")[1]; // Assuming `id` is unique for each station
    const arrive = secondSelectedNode.data("id").split("-")[1];

    console.log(`Requesting parcours from ${depart} to ${arrive}`);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/dijkstra?s1=${depart}&s2=${arrive}`
      );

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      console.log(response);
      const data = await response.json();
      console.log(data);
      showparcours(data);
    } catch (error) {
      console.error("Failed to fetch parcours:", error);
    }
  } else {
    console.error("Please select departure and destination stations.");
  }
}

function showparcours(data) {
  const itineraryContainer = document.getElementById("itinerary");
  const timeInfo = document.getElementById("time");

  if (!data || !data.data) {
    console.error("Invalid data received from the backend.");
    itineraryContainer.innerHTML = "<li>No route found.</li>";
    timeInfo.textContent = "";
    return;
  }

  // Extract response data
  const steps = data.data.itineraire || [];
  const stations = data.data.stations || [];
  const totalTime = data.data.temps || 0;

  // Clear previous content
  itineraryContainer.innerHTML = "";
  timeInfo.textContent = "";

  // Display the itinerary steps
  if (steps.length > 0) {
    steps.forEach((step) => {
      const stepElement = document.createElement("li");
      stepElement.textContent = step;
      itineraryContainer.appendChild(stepElement);
    });
  } else {
    const noStepsElement = document.createElement("li");
    noStepsElement.textContent = "No itinerary steps available.";
    itineraryContainer.appendChild(noStepsElement);
  }

  // Display the total time
  timeInfo.textContent =
    totalTime > 0
      ? `Estimated travel time: ${Math.round(totalTime / 60)} minutes`
      : "Travel time unavailable";

  // Highlight the path on the graph
  highlightPath(stations);
}

function highlightPath(stations) {
  console.log("Stations data for highlighting:", stations);

  if (!cy || typeof cy.elements !== "function") {
    console.error("Invalid Cytoscape instance passed to highlightPath.");
    return;
  }

  // Reset all highlights
  cy.elements().removeClass("highlighted");

  if (!Array.isArray(stations) || stations.length === 0) {
    console.warn("No stations to highlight.");
    return;
  }

  // Highlight nodes and edges along the path
  stations.forEach(([source, target]) => {
    const prefixedSource = `station-${source}`;
    const prefixedTarget = `station-${target}`;

    console.log(
      `Highlighting edge from ${prefixedSource} to ${prefixedTarget}`
    );

    const edge = cy.edges(
      `[source="${prefixedSource}"][target="${prefixedTarget}"]`
    );
    const sourceNode = cy.nodes(`#${prefixedSource}`);
    const targetNode = cy.nodes(`#${prefixedTarget}`);

    console.log("Edge found:", edge.data());
    console.log("Source node found:", sourceNode.data());
    console.log("Target node found:", targetNode.data());

    if (edge.length) edge.addClass("highlighted");
    if (sourceNode.length) sourceNode.addClass("highlighted");
    if (targetNode.length) targetNode.addClass("highlighted");
  });

  // Optionally fit view to the highlighted path
  const highlightedElements = cy.elements(".highlighted");
  if (highlightedElements.length > 0) {
    cy.fit(highlightedElements, 50); // Fit view with padding
  }
}

async function kruskal() {

  console.log(`Requesting Kruskal`);

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/kruskal`
    );

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    console.log(response);
    const data = await response.json();
    console.log(data);
    showparcours(data);
  } catch (error) {
    console.error("Failed to fetch parcours:", error);
  }
  console.error("Please select departure and destination stations.");
}
