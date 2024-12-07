import cy from "./cytoscape.js";


let departStation = null;
let arriveStation = null;

// DOM elements

const selectedStationsDisplay = document.getElementById("selectedStations");
const fastestPathDisplay = document.getElementById("fastestPath");
const stationList = document.getElementById("stationList");

parcoursButton.addEventListener("click", toggleParcoursMode);
stationList.addEventListener("click", onStationListClick);

/**
 * Toggles the Parcours mode on or off.
 */


/**
 * Resets the current selections and UI updates when Parcours mode is turned off.
 */
function resetSelections() {
  // Clear departure station
  if (departStation) {
    const departNode = cy.$(`node[name="${departStation}"]`);
    departNode.data("depart", "False");
  }

  // Clear arrival station
  if (arriveStation) {
    const arriveNode = cy.$(`node[name="${arriveStation}"]`);
    arriveNode.data("destination", "False");
  }

  departStation = null;
  arriveStation = null;

  updateUI();
}

/**
 * Handles station selection triggered by clicking on a station name in the list.
 * @param {MouseEvent} event The click event on the station list.
 */
function onStationListClick(event) {
  if (event.target && event.target.tagName === "LI") {
    const stationName = event.target.textContent.split(" (")[0];
    handleStationSelection(stationName);
  }
}

/**
 * Manages the logic of selecting or deselecting departure/arrival stations.
 * @param {string} stationName The name of the station selected.
 */
function handleStationSelection(stationName) {
  const stationNode = cy.elements(`[name="${stationName}"]`);

  if (stationNode.empty()) {
    console.warn(`No station found for name: ${stationName}`);
    return;
  }

  // If no departure yet, set this as departure
  if (!departStation) {
    departStation = stationName;
    stationNode.data("depart", "True");
    stationNode.data("destination", "False");

    // If no arrival yet and it's different from departure, set as arrival
  } else if (!arriveStation && stationName !== departStation) {
    arriveStation = stationName;
    stationNode.data("destination", "True");
    stationNode.data("depart", "False");

    // If clicking again on the departure station, deselect it
  } else if (stationName === departStation) {
    const prevDepartNode = cy.$(`node[name="${departStation}"]`);
    prevDepartNode.data("depart", "False");
    departStation = null;

    // If clicking again on the arrival station, deselect it
  } else if (stationName === arriveStation) {
    const prevArriveNode = cy.$(`node[name="${arriveStation}"]`);
    prevArriveNode.data("destination", "False");
    arriveStation = null;
  }

  updateUI();

  // If both stations are selected, we could proceed to path calculation (TODO)
  if (departStation && arriveStation) {
    // TODO: send selected stations to backend or perform path calculation
  }
}

/**
 * Updates the UI to reflect the currently selected stations.
 */
function updateUI() {
  selectedStationsDisplay.textContent = `Selected: ${
    departStation || "None"
  } -> ${arriveStation || "None"}`;
  fastestPathDisplay.textContent = "Path: None";
}
