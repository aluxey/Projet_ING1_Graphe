import { initCytoscape } from "./cytoscapeInit.js";

document.addEventListener("DOMContentLoaded", async () => {
  await initCytoscape();

  if (!cy) {
    console.error("Cytoscape was not initialized properly.");
    return;
  }

});
