let firstSelectedNode = null;
let secondSelectedNode = null;

let departureStation = null;
let destinationStation = null;
let parcoursButton = null;

document.addEventListener("DOMContentLoaded", () => {
  // Initialize DOM elements
  departureStation = document.getElementById("depart");
  destinationStation = document.getElementById("arrive");
  parcoursButton = document.getElementById("parcoursButton");

  if (!departureStation || !destinationStation || !parcoursButton) {
    console.error("Required DOM elements not found!");
    return;
  }

  // Attach event to the parcours button
  parcoursButton.addEventListener("click", parcours);
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
function parcours() {
  if (firstSelectedNode && secondSelectedNode) {
    const depart = firstSelectedNode.data("name");
    const arrive = secondSelectedNode.data("name");

    console.log(`Parcours from ${depart} to ${arrive}`);
  } else {
    console.error("Please select departure and destination stations.");
  }
}
