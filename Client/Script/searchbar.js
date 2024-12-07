const searchInput = document.getElementById("search");
const stationList = document.getElementById("stationList");

let stations = [];
let lines = [];

// Initialize data on page load
initializeData();
searchInput.addEventListener("input", onSearchInput);

/**
 * Loads station data from the server and stores it locally.
 */
async function initializeData() {
  try {
    const data = await fetchMetroData();
    stations = data.stations || [];
    lines = data.lines || [];
    console.log("Stations and lines loaded:", stations, lines);
  } catch (error) {
    console.error("Error initializing metro data:", error);
    alert("Failed to load metro data. Please try again later.");
  }
}

/**
 * Fetches the merged data from the server.
 * @returns {Promise<Object>} The JSON containing stations and lines.
 */
async function fetchMetroData() {
  const response = await fetch("/Server/Data/merged_data.json");
  if (!response.ok) throw new Error("Failed to fetch station data");
  return response.json();
}

/**
 * Handler for search input change events.
 * @param {Event} event The input event from the search field.
 */
function onSearchInput(event) {
  const query = event.target.value;
  const filteredStations = filterStations(query);
  updateSearchResults(filteredStations);
}

/**
 * Filters stations by query matching station name or line.
 * @param {string} query The search query from the user.
 * @returns {Array} List of stations that match the query.
 */
function filterStations(query) {
  const lowerQuery = query.toLowerCase().trim();

  return stations.filter(
    (station) =>
      station.name.toLowerCase().includes(lowerQuery) ||
      station.ligne.toLowerCase().includes(lowerQuery)
  );
}

/**
 * Updates the displayed station list based on search results.
 * @param {Array} results The filtered list of stations.
 */
function updateSearchResults(results) {
  stationList.innerHTML = "";

  if (results.length === 0) {
    stationList.innerHTML = "<li>No stations found</li>";
    return;
  }

  results.forEach((station) => {
    const stationItem = document.createElement("li");
    stationItem.textContent = `${station.name} (Line ${station.ligne})`;
    stationList.appendChild(stationItem);
  });
}
