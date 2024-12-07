let firstSelectedNode = null;
let secondSelectedNode = null;

const departureStation = document.getElementById("depart");
const destinationStation = document.getElementById("arrive");

export function addCytoscapeEvents(cy) {
  const tooltip = document.getElementById("tooltip");

  cy.on("mouseover", "node", (event) => showTooltip(event.target, tooltip));
  cy.on("mouseout", "node", () => hideTooltip(tooltip));
  cy.on("mousemove", (event) => moveTooltip(event, tooltip));
  cy.on("click", "node", (event) => handleNodeClick(event.target));
}

function showTooltip(node, tooltip) {
  tooltip.style.display = "block";
  tooltip.innerHTML = `
    <strong>${node.data("name")}</strong><br>
    Ligne: ${node.data("ligne")}<br>
    Terminus: ${node.data("terminus") === "True" ? "Oui" : "Non"}
  `;
}

function hideTooltip(tooltip) {
  tooltip.style.display = "none";
}

function moveTooltip(event, tooltip) {
  tooltip.style.left = `${event.originalEvent.pageX + 10}px`;
  tooltip.style.top = `${event.originalEvent.pageY + 10}px`;
}

function handleNodeClick(node) {
  if (!firstSelectedNode) {
    selectFirstNode(node);
  } else if (!secondSelectedNode && node !== firstSelectedNode) {
    selectSecondNode(node);
  } else {
    resetAndSelectFirstNode(node);
  }
}

function selectFirstNode(node) {
  firstSelectedNode = node;
  firstSelectedNode.data("depart", "True");
  firstSelectedNode.data("destination", "False");
  departureStation.innerHTML =
    firstSelectedNode.data("name") +
    " ( Line " +
    firstSelectedNode.data("ligne") +
    " )";
}

function selectSecondNode(node) {
  secondSelectedNode = node;
  secondSelectedNode.data("destination", "True");
  secondSelectedNode.data("depart", "False");
  destinationStation.innerHTML =
    secondSelectedNode.data("name") +
    " ( Line " +
    secondSelectedNode.data("ligne") +
    " )";
}

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
  alert("Départ sélectionné: " + firstSelectedNode.data("name"));
}
