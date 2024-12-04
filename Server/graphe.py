from collections import defaultdict
from dataclasses import dataclass
from difflib import diff_bytes
from typing import List, Dict, Set, DefaultDict, Optional, Tuple
import json
import os
from pathlib import Path
from typing import Dict

@dataclass
class Station:
    id: int
    name: str
    ligne: Dict[str, str]
    terminus: bool
    voisins: List[Tuple["Station", int]]

    # Implémentation de la méthode __hash__ pour rendre l'objet hashable
    def __hash__(self):
        return hash((self.id, self.name))

    # Implémentation de la méthode __eq__ pour comparer deux objets Station
    def __eq__(self, other):
        if isinstance(other, Station):
            return self.id == other.id and self.name == other.name
        return False

    def __str__(self):
        # Retourne une chaîne de caractères pour l'affichage
        voisins_str = ", ".join([f"{v[0].name}({v[0].id})" for v in self.voisins])
        return (f"Station(id={self.id}, "
                f"name={self.name}, "
                f"lignes={self.ligne}, "
                f"terminus={'Oui' if self.terminus else 'Non'}, "
                f"voisins=[{voisins_str}])")

    def __repr__(self):
        return self.__str__()

    def get_essential_info(self):
        return f"{self.name} ({self.id})"

@dataclass
class Edge:
    start: int
    end: int
    time: int

@dataclass
class Position:
    posX: float
    posY: float
    nom_station: str

class MetroNetwork:
    def __init__(self, input_file: str, positions_file: str):
        self.input_file = Path(input_file)
        self.positions_file = Path(positions_file)
        self.stations: List[Dict] = []
        self.edges: List[Dict] = []
        self.positions: List[Dict] = []
        self.graph: DefaultDict = defaultdict(list)

    def process_metro_file(self) -> None:
        """Process the metro network file containing stations and connections."""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    if line.startswith('V'):
                        self._process_station(line)
                    elif line.startswith('E'):
                        self._process_edge(line)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{self.input_file}' not found")
        except Exception as e:
            raise Exception(f"Error processing metro file: {str(e)}")

    def _process_station(self, line: str) -> None:
        """Process a station line and add it to stations list."""
        try:
            parts = line.split(' ;')
            desc = parts[0].split(' ', 2)
            station = {
                "id": int(desc[1]),
                "name": desc[2],
                "ligne": parts[1],
                "terminus": parts[2].split(' ', 2)[0],
                "branchement": parts[2].split(' ', 2)[1]
            }
            self.stations.append(station)
        except (IndexError, ValueError) as e:
            print(f"Error processing station line: {line}\n{e}")

    def _process_edge(self, line: str) -> None:
        """Process an edge line and add it to edges list."""
        try:
            _, start, end, time = line.split()
            edge = {
                "start": int(start.strip()),
                "end": int(end.strip()),
                "time": int(time.strip())
            }
            self.edges.append(edge)
        except ValueError as e:
            print(f"Error processing edge line: {line}\n{e}")

    def process_positions(self) -> None:
        """Process the positions file containing station coordinates."""
        try:
            with open(self.positions_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split(';')
                    if len(parts) >= 3:
                        position = {
                            "posX": float(parts[0].strip()),
                            "posY": float(parts[1].strip()),
                            "nom_station": parts[2].strip()
                        }
                        self.positions.append(position)
                    else:
                        print(f"Skipped invalid line: {line}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Positions file '{self.positions_file}' not found")

    def build_graph(self) -> None:
        """Build an undirected graph representation of the metro network."""
        self.graph = defaultdict(list)
        for edge in self.edges:
            start, end, time = edge["start"], edge["end"], edge["time"]
            self.graph[start].append({"node": end, "time": time})
            self.graph[end].append({"node": start, "time": time})

    def is_connected(self) -> bool:
        """Check if the metro network graph is connected using BFS."""
        if not self.graph:
            return False

        visited: Set[int] = set()
        start_node = next(iter(self.graph.keys()))
        queue = [start_node]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                queue.extend(
                    neighbor["node"] for neighbor in self.graph[node]
                    if neighbor["node"] not in visited
                )

        return len(visited) == len(set(station["id"] for station in self.stations))

    def save_to_json(self, output_file: str) -> None:
        """Save the metro network data to a JSON file."""
        self.stations.sort(key=lambda x: x["name"].lower())
        data = {
            "stations": self.stations,
            "edges": self.edges,
        }
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data saved to '{output_file}'")

    def save_positions_to_json(self, output_file: str) -> None:
        """Save the positions data to a JSON file."""
        self.positions.sort(key=lambda x: x["nom_station"].lower())
        data = {"positions": self.positions}
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Position data saved to '{output_file}'")

    def display_graph(self) -> None:
        """Display the metro network graph structure."""
        station_dict = {station["id"]: station for station in self.stations}
        for node, neighbors in self.graph.items():
            station = station_dict.get(node, {"name": "Unknown"})
            print(f"\nStation {node} ({station['name']}):")
            for neighbor in neighbors:
                neighbor_station = station_dict.get(neighbor["node"], {"name": "Unknown"})
                print(f"  → {neighbor['node']} ({neighbor_station['name']}) "
                      f"[Time: {neighbor['time']} seconds]")

def main():
    try:
        # Initialize the metro network
        metro = MetroNetwork('metro.txt', 'pospoints.txt')
        
        # Process input files
        print("Processing metro network file...")
        metro.process_metro_file()
        
        print("\nProcessing positions file...")
        metro.process_positions()
        
        # Build and analyze the graph
        print("\nBuilding metro network graph...")
        metro.build_graph()
        
        print("\nDisplaying metro network structure:")
        metro.display_graph()
        
        # Check if the network is connected
        if metro.is_connected():
            print("\nThe metro network is connected.")
        else:
            print("\nWarning: The metro network is not connected!")
        
        # Save processed data
        metro.save_to_json('sorted_metro.json')
        metro.save_positions_to_json('pospoints.json')
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


def dijkstra(depart: Station, arrivee: Station):
    # Pour chaque id station : id station provenance + le temps pour arriver à la station en question depuis le debut
    stations: {int: Tuple[int, int]} = {}
    # Liste des id stations déjà traitées
    stations_traitees: List[int] = []
    # id station : le temps pour arriver à cette station
    current_station: Tuple[int, int] = (depart.id, 0)

    no_station_available: bool = False

    while current_station[0] != arrivee.id and not no_station_available:
        stations_traitees.append(current_station[0])

        real_station = get_station_by_id(current_station[0])
        # parcours les stations voisines pour modifier leur parcours
        for neighbor_station in real_station.voisins:
            # ne traite pas le sommet de depart
            if neighbor_station[0].id != debut.id:
                # pas encore ajouté
                if stations.get(neighbor_station[0].id) is None:
                    stations[neighbor_station[0].id] = (current_station[0], current_station[1] + neighbor_station[1])
                else:
                    # modifie la station précédente si c'est plus rapide avec ce chemin qu'avec l'ancien
                    potential_new_time: int = current_station[1] + neighbor_station[1]
                    if potential_new_time < stations[neighbor_station[0].id][1]:
                        stations[neighbor_station[0].id] = [current_station[0], potential_new_time]
        # choisi la nouvelle station à traiter
        selected_station: [int, int] = None
        for station in stations.keys():
            if station not in stations_traitees:
                if selected_station is None:
                    selected_station = (station, stations[station][1])
                else:
                    if stations[station][1] < selected_station[1]:
                        selected_station = (station, stations[station][1])
        if selected_station is None:
            no_station_available = True
        else:
            current_station = selected_station

    # gerer le cas où dijkstra plante :
    if no_station_available:
        return None
    return stations


def get_station_by_id(station_id):
    for station in all_stations:
        if station.id == station_id:
            return station
    return None

# if __name__ == "__main__":
#     main()


quinconces: Station = Station(1, "quinconces", {"3": "0"}, True, [])
debut: Station = Station(2, "debut", {"3": "0"}, False, [])
republique: Station = Station(3, "repblique", {"3": "0"}, False, [])
eglise: Station = Station(4, "eglise", {"3": "2"}, False, [])
issac: Station = Station(5, "issac", {"3": "2"}, True, [])
zola: Station = Station(6, "zola", {"3": "1"}, False, [])
lycee: Station = Station(7, "lycee", {"3": "1", "84": "0"}, False, [])
villepreux: Station = Station(8, "villepreux", {"3": "1"}, True, [])
proust: Station = Station(9, "proust", {"84": "0"}, True, [])
cantinole: Station = Station(10, "cantinole", {"84": "0"}, False, [])
fin: Station = Station(11, "fin", {"84": "2"}, False, [])
rostand: Station = Station(12, "rostand", {"84": "2"}, True, [])
cinq_chemins: Station = Station(13, "5 chemins", {"84": "1"}, False, [])
aeroport: Station = Station(14, "aeroport", {"84": "1"}, True, [])

quinconces.voisins.append((debut, 2))
debut.voisins.append((quinconces, 2))
debut.voisins.append((republique, 3))
republique.voisins.append((debut, 3))
republique.voisins.append((eglise, 2))
republique.voisins.append((zola, 1))
eglise.voisins.append((republique, 3))
eglise.voisins.append((issac, 1))
issac.voisins.append((eglise, 1))
zola.voisins.append((republique, 1))
zola.voisins.append((lycee, 2))
lycee.voisins.append((zola, 2))
lycee.voisins.append((villepreux, 2))
lycee.voisins.append((proust, 1))
lycee.voisins.append((cantinole, 1))
villepreux.voisins.append((lycee, 2))
proust.voisins.append((lycee, 1))
cantinole.voisins.append((lycee, 1))
cantinole.voisins.append((fin, 3))
cantinole.voisins.append((cinq_chemins, 3))
fin.voisins.append((cantinole, 3))
fin.voisins.append((rostand, 2))
rostand.voisins.append((fin, 2))
cinq_chemins.voisins.append((cantinole, 3))
cinq_chemins.voisins.append((aeroport, 2))
aeroport.voisins.append((cinq_chemins, 2))

all_stations = [quinconces, debut, republique, eglise, issac, zola, lycee, villepreux, proust, cantinole, fin, rostand,
                cinq_chemins, aeroport]



stations_test = dijkstra(debut, fin)
if stations_test is None:
    print("envie de creuver")
else:
    print(stations_test)