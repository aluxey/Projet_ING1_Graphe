let departStation = null;
let arriveStation = null;
let isParcoursMode = false; // Track toggle state

const parcoursButton = document.getElementById("toggleParcours");

parcoursButton.addEventListener("click", () => {
  isParcoursMode = !isParcoursMode;
  document.getElementById("parcoursStatus").textContent = `Parcours Mode: ${isParcoursMode ?"On" : "Off"}`;

  // Reset selections if exiting Parcours Mode
  if (!isParcoursMode) {
    departStation = null;
    arriveStation = null;

    document.getElementById("selectedStations").textContent = "Selected: None";
    document.getElementById("fastestPath").textContent = "Path: None";
  }
});


// Function to handle station clicks
function handleStationClick(stationName) {
  if (!isParcoursMode) return; // Only allow selection in Parcours Mode

  if (!departStation) {
    departStation = stationName;
  } else if (!arriveStation && stationName !== departStation) {
    arriveStation = stationName;
  }

  // Update the UI with the current selections
  document.getElementById("selectedStations").textContent = `Selected: ${departStation || "None"} -> ${arriveStation || "None"}`;

  // If both stations are selected, calculate the path
  if (departStation && arriveStation) {
    alert("Calculating path... (ca va arriver un jour insh)");
  }
}

// Add event listeners to station list items
document.getElementById("stationList").addEventListener("click", (event) => {
  const stationName = event.target.textContent.split(" (")[0]; // Extract station name
  handleStationClick(stationName);
});