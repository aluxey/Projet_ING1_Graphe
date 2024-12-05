async function loadMetroData() {
  const response = await fetch("/Server/Data/merged_data.json");
  if (!response.ok) throw new Error("Failed to fetch station data");
  return response.json();
}

const searchInput = document.getElementById("search");
const stationList = document.getElementById("stationList");
const lineList = document.getElementById("lineList");

let stations = [];
let lines = [];


/**
 * Initialize the search bar by loading the metro data
 */
async function initialize() {
  try {
    const data = await loadMetroData();
    stations = data.stations || [];
    lines = data.lines || [];
    console.log("Stations and lines loaded:", stations, lines);
  } catch (error) {
    console.error("Error initializing metro data:", error);
    alert("Failed to load metro data. Please try again later.");
  }
}

/**
 * Filter the stations based on the search query
 * @param {*} query  What the user type in the search bar
 * @returns The stations that match the search query
 */
function filterStations(query) {
  const lowerQuery = query.toLowerCase().trim();

  return stations.filter(
    (station) =>
      station.name.toLowerCase().includes(lowerQuery) || // Match station name
      station.ligne.toLowerCase().includes(lowerQuery) // Match line
  );
}

/**
 * 
 * @param {*} results 
 * @returns 
 */
// Function to update the displayed search results
function updateSearchResults(results) {
    // Clear previous results
    stationList.innerHTML = "";

    if (results.length === 0) {
        stationList.innerHTML = "<li>No stations found</li>";
        return;
    }

    // Populate station list with station name and line
    results.forEach((station) => {
        const stationItem = document.createElement("li");
        stationItem.textContent = `${station.name} (Line ${station.ligne})`;
        stationList.appendChild(stationItem);
    });
}

// Event listener for the search input
searchInput.addEventListener("input", (event) => {
  const query = event.target.value;
  const filteredStations = filterStations(query);
  updateSearchResults(filteredStations);
});

// Initialize the data when the page loads
initialize();