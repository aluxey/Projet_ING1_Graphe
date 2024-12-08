export const colorLine = {
  1: "#FFCD00",
  2: "#003CA6",
  3: "#837902",
  3_1: "#6EC4E8",
  4: "#CF009E",
  5: "#FF7E2E",
  6: "#6ECA97",
  7: "#FA9ABA",
  7_1: "#6CAEDF",
  8: "#E19BDF",
  9: "#B6BD00",
  10: "#C9910D",
  11: "#704B1C",
  12: "#007852",
  13: "#6EC4E8",
  14: "#62259D",
};

export const cyStyle = [
  // Style de base pour les nœuds
  {
    selector: "node",
    style: {
      "background-color": "#fff",
      "border-color": (ele) => colorLine[ele.data("ligne")] || "#000",
      "border-width": "2px",
      width: "8px",
      height: "8px",
      shape: "ellipse",
    },
  },
  // Station de départ
  {
    selector: 'node[depart = "True"]',
    style: {
      "background-color": "#00FF00", // Vert pour le départ
      "border-width": "4px",
      width: "25px",
      height: "25px",
    },
  },
  // Station d'arrivée
  {
    selector: 'node[destination = "True"]',
    style: {
      "background-color": "#FF0000", // Rouge pour l'arrivée
      "border-width": "4px",
      width: "25px",
      height: "25px",
    },
  },
  // Stations terminus
  {
    selector: 'node[terminus = "True"]',
    style: {
      "background-color": "#fff",
      "border-color": (ele) => colorLine[ele.data("ligne")] || "#000",
      "border-width": "4px",
      width: "12px",
      height: "12px",
      shape: "rectangle",
    },
  },
  // Style de base pour les arêtes
  {
    selector: "edge",
    style: {
      width: 2,
      "line-color": (ele) => colorLine[ele.data("ligne")] || "#ccc",
      "curve-style": "bezier",
    },
  },
  // Nœuds surlignés (changés en couleur uniquement)
  {
    selector: ".highlightedStations",
    style: {
      "background-color": "#FFFF00", // Jaune pour les nœuds surlignés
      "border-width": "2px", // Garde une bordure fine
      "border-color": "#FFA500", // Orange clair pour la bordure
    },
  },
  // Arêtes surlignées (sans flèches, avec une couleur distincte)
  {
    selector: ".highlightedAretes",
    style: {
      "line-color": "#FF4500", // Orange vif pour les arêtes surlignées
      width: 4, // Plus épais pour les distinguer
    },
  },
  // Nœuds et arêtes surlignés (général)
  {
    selector: ".highlighted",
    style: {
      "background-color": "#87CEFA", // Bleu clair pour les nœuds
      "line-color": "#FF6347", // Rouge clair pour les arêtes
      "border-color": "#4682B4", // Bleu foncé pour les nœuds
      "border-width": "3px",
      width: "10px",
      height: "10px",
    },
  },
];
