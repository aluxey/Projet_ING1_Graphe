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
async function parcours() {
  if (firstSelectedNode && secondSelectedNode) {
    const depart = firstSelectedNode.data("id"); // Assuming `id` is unique for each station
    const arrive = secondSelectedNode.data("id");

    console.log(`Requesting parcours from ${depart} to ${arrive}`);

    try {
      const response = await fetch(`http://127.0.0.1:5000/dijkstra`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          depart,
          arrive,
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      showparcours(data); // Pass the data to a rendering function
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
    return;
  }

  // Clear previous content
  itineraryContainer.innerHTML = "";
  timeInfo.textContent = "";

  // Display the itinerary steps
  const steps = data.data.itineraire;
  steps.forEach((step) => {
    const stepElement = document.createElement("li");
    stepElement.textContent = step;
    itineraryContainer.appendChild(stepElement);
  });

  // Display the total time
  const totalTime = data.data.temps;
  timeInfo.textContent = `You will take ${Math.round(
    totalTime / 60
  )} minutes to reach your destination.`;
}
