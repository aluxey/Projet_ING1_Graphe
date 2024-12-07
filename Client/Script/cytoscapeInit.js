import cytoscape from "https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.21.1/cytoscape.esm.min.js";
import { cyStyle } from "./config.js";
import { loadMetroData, buildElements } from "./data.js";
import { addCytoscapeEvents } from "./events.js";

export let cy = null; // Export so other files can use it if needed

export async function initCytoscape() {
  const data = await loadMetroData();
  const elements = buildElements(data);

  cy = cytoscape({
    container: document.getElementById("cy"),
    elements,
    style: cyStyle,
    layout: { name: "preset" },
  });

  addCytoscapeEvents(cy);
}
