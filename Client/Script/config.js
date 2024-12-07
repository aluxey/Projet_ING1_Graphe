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
  {
    selector: 'node[depart = "True"]',
    style: {
      "background-color": "#00FF00",
      "border-width": "4px",
      width: "25px",
      height: "25px",
    },
  },
  {
    selector: 'node[destination = "True"]',
    style: {
      "background-color": "#FF0000",
      "border-width": "4px",
      width: "25px",
      height: "25px",
    },
  },
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
  {
    selector: "edge",
    style: {
      width: 2,
      "line-color": (ele) => colorLine[ele.data("ligne")] || "#ccc",
      "curve-style": "bezier",
      "font-size": "6px",
      "font-weight": "bold",
    },
  },
];
