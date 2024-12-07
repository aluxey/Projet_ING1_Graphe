

export async function loadMetroData() {
  const response = await fetch("/Server/Data/merged_data.json");
  return await response.json();
}

export function buildElements(data) {
  const nodes = data.stations.map((station) => ({
    data: {
      id: `station-${station.id}`,
      name: station.name,
      ligne: station.ligne,
      terminus: station.terminus,
      depart: "False",
      destination: "False",
    },
    position: {
      x: station.posX || Math.random() * 1000,
      y: station.posY || Math.random() * 1000,
    },
  }));

  const edges = data.edges.map((edge) => ({
    data: {
      id: `edge-${edge.start}-${edge.end}`,
      source: `station-${edge.start}`,
      target: `station-${edge.end}`,
      time: edge.time,
      ligne: data.stations.find((s) => s.id === edge.start)?.ligne || null,
    },
  }));

  return [...nodes, ...edges];
}
