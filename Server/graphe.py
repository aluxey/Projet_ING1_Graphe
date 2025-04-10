from dataclasses import dataclass
from typing import List, Dict, Tuple


from flask import Flask, request, jsonify
from flask_cors import CORS

@dataclass
class Station:
    id: int
    name: str
    # ligne : embranchement
    lignes: Dict[str, str]
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
                f"lignes={self.lignes}, "
                f"terminus={'Oui' if self.terminus else 'Non'}, "
                f"voisins=[{voisins_str}])")

    def __repr__(self):
        return self.__str__()

    def get_essential_info(self):
        return f"{self.name} ({self.id})"

def get_connexe(test_stations, missing_stations, station: Station):
    for voisin in station.voisins:
        if voisin[0] not in test_stations:
            test_stations.append(voisin[0])
            missing_stations.remove(voisin[0])
            get_connexe(test_stations, missing_stations, voisin[0])

def creer_connexite():
    init = all_stations[0]
    test_stations = [init]
    missing_stations = all_stations.copy()
    missing_stations.remove(init)
    get_connexe(test_stations, missing_stations, init)

    station_test = next((station for station in all_stations if station not in missing_stations), None)
    for station in missing_stations:
        station.voisins.append((station_test, 1000))
        station_test.voisins.append((station, 1000))

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

        real_station = get_station_by_id(current_station[0], all_stations)
        # parcours les stations voisines pour modifier leur parcours
        for neighbor_station in real_station.voisins:
            neighbor_id = neighbor_station[0].id
            neighbor_time_travel = neighbor_station[1]

            # ne traite pas le sommet de depart
            if neighbor_id != depart.id:
                # pas encore ajouté
                if stations.get(neighbor_id) is None:
                    stations[neighbor_id] = (current_station[0], current_station[1] + neighbor_time_travel)
                else:
                    # modifie la station précédente si c'est plus rapide avec ce chemin qu'avec l'ancien
                    potential_new_time: int = current_station[1] + neighbor_time_travel
                    if potential_new_time < stations[neighbor_id][1]:
                        stations[neighbor_id] = [current_station[0], potential_new_time]
        # choisi la nouvelle station à traiter
        selected_station: (int, int) = None
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

def get_station_by_id(station_id: int, stations_to_search_in: List[Station]):
    for station in stations_to_search_in:
        if station.id == station_id:
            return station
    return None

def calcul_direction(deja_vu: List, lst_terminus: set, current: Station, final_dest: Station, ligne: str, trouve: bool, branchement_initial: str):
    new_trouve = trouve or current.id == final_dest.id
    
    deja_vu.append(current.id)
    for voisin in current.voisins:
        if (voisin[0].id not in deja_vu) and (ligne in voisin[0].lignes.keys()):
            # si on est initialement sur le branchement 0
            # OU on arrive sur le branchement 0
            # OU on est sur le meme branchement
            if branchement_initial == "0" or voisin[0].lignes[ligne] == "0" or branchement_initial == voisin[0].lignes[ligne]:
                if voisin[0].terminus:
                    if new_trouve or voisin[0].id == final_dest.id:
                        lst_terminus.add(voisin[0].name)
                else:
                    calcul_direction(deja_vu, lst_terminus, voisin[0], final_dest, ligne, new_trouve, branchement_initial)

def get_all_possible_destinations(first_station: Station, last_station: Station, ligne: str):
    terminus = set()
    calcul_direction([], terminus, first_station, last_station, ligne, False, first_station.lignes[ligne])
    return terminus

def get_ligne_optimale(dijkstra: {int: Tuple[int, int]}, initial: Station):
    current = initial
    lst_lignes = set(current.lignes.keys())
    while len(lst_lignes) != 0 or len(lst_lignes) != 1:
        current = get_station_by_id(dijkstra[current.id][0], all_stations)
        lst_lignes_suivantes = lst_lignes & current.lignes.keys()
        if len(lst_lignes_suivantes) == 1:
            return next(iter(lst_lignes_suivantes)) # taille 1, donc le seul élément
        if len(lst_lignes_suivantes) == 0:
            return next(iter(lst_lignes)) # n'importe laquelle des lignes
        lst_lignes = lst_lignes_suivantes
    if len(lst_lignes) == 1:
        return lst_lignes[0]
    if len(lst_lignes) == 0:
        return None


def choix_lignes(dijkstra: {int: Tuple[int, int]}, arrivee: int):
    ligne_choisie: str = ""
    ligne_par_arret: [(int, str)] = []
    current = get_station_by_id(arrivee, all_stations)
    ligne_par_arret.append((current.id, get_ligne_optimale(dijkstra, current)))
    while current.id in dijkstra:
        x = get_station_by_id(dijkstra[current.id][0], all_stations)
        lignes_possible = current.lignes.keys() & x.lignes.keys()
        if len(lignes_possible) == 0: # pas de ligne commune -> besoin de marcher
            ligne_choisie = get_ligne_optimale(dijkstra, x)
            ligne_par_arret.append((x.id, ligne_choisie + "-marche"))
        else:
            if ligne_choisie not in lignes_possible: # la ligne courante n'est plus sur le trajet -> besoin de changer de metro
                ligne_choisie = get_ligne_optimale(dijkstra, current)
            ligne_par_arret.append((x.id, ligne_choisie))
        current = x
    return ligne_par_arret


def doit_changer_direction(init: int, next: int, ligne: str):
    # si init et next sont sur le meme branchement
    init_station = get_station_by_id(init, all_stations)
    next_station = get_station_by_id(next, all_stations)
    if init_station.lignes[ligne] == next_station.lignes[ligne]:
        return False

    # si on est initialement sur le branchement 0
    if init_station.lignes[ligne] == "0":
        return False

    # si on arrive sur le branchement 0
    if next_station.lignes[ligne] == "0":
        return False

    # si on arrive sur un autre branchement que 0 et qu'on vient d'un autre branchement que 0
    return True




def get_full_itineraire(choix_l: [(int, str)], temps: int):
    itineraire: List[str] = []
    choix_lignes = choix_l
    choix_lignes.reverse()
    index_parcours = 0
    init = choix_lignes[index_parcours]
    fin = choix_lignes[0]
    ligne = init[1]
    doit_marcher = False
    index_parcours += 1
    est_fini = False
    next = choix_lignes[index_parcours]
    affiche_indication = False
    itineraire.append(f"Débutez à la station {get_station_by_id(init[0], all_stations).name}")
    while not est_fini:
        init_station = get_station_by_id(init[0], all_stations)
        fin_station = get_station_by_id(fin[0], all_stations)
        if next[1] == init[1] or next[1].startswith(init[1] + "-"): # on peut rester sur la meme ligne
            if doit_changer_direction(init[0], next[0], ligne):
                itineraire.append(
                    f"Prenez la ligne {ligne} direction {' ou '.join(get_all_possible_destinations(init_station, fin_station, ligne))} jusqu'à {fin_station.name}"
                )

                init = fin
            fin = next
            if next[1].startswith(init[1] + "-"):
                doit_marcher = True
        else: # changement de ligne
            next_station = get_station_by_id(next[0], all_stations)
            if doit_marcher:
                directions = " ou ".join(get_all_possible_destinations(init_station, fin_station, ligne))
                itineraire.append(f"Prenez la ligne {ligne} direction {directions} jusqu'à {fin_station.name}")
                itineraire.append(f"Marchez jusqu'à la station {next_station.name}")
            else:
                directions = " ou ".join(get_all_possible_destinations(init_station, fin_station, ligne))
                itineraire.append(f"Prenez la ligne {ligne} direction {directions} jusqu'à {next_station.name}")
            affiche_indication = True
            init = next
            ligne = init[1].split("-", 1)[0]
            doit_marcher = False
        if index_parcours == (len(choix_lignes) - 1): # si on est sur le dernier sommet
            next_station = get_station_by_id(next[0], all_stations)
            if not affiche_indication:
                directions = " ou ".join(get_all_possible_destinations(init_station, fin_station, ligne))
                itineraire.append(f"Prenez la ligne {ligne} direction {directions} jusqu'à {fin_station.name}")
            itineraire.append(f"Vous devriez arriver à {next_station.name} en {temps} secondes")
            est_fini = True
        else:
            affiche_indication = False
            index_parcours += 1
            next = choix_lignes[index_parcours]
    return itineraire

def prim(depart: Station):
    non_vu = []
    deja_vu: List[Station] = []
    aretes: [[int, int]] = []

    for station in all_stations:
        non_vu.append(station.id)

    current = depart
    deja_vu.append(current)
    non_vu.remove(current.id)
    while len(non_vu) > 0:
        # liste de Tuple(station1, station2, cout)
        arretes_eligibles: List[Tuple[Station, Station, int]] = []
        # toutes les stations deja_vu
        for station in deja_vu:
            # tous les voisins de ces stations
            for voisin in station.voisins:
                # voisin non_vu = ne fait pas de boucle
                if voisin[0].id in non_vu:
                    # arrete entre la station et son voisin est éligible
                    arretes_eligibles.append((station, voisin[0], voisin[1]))
        if len(arretes_eligibles) > 0:
            # tri les aretes par cout croissant
            arretes_eligibles.sort(key=lambda x: x[2])
            aretes.append([arretes_eligibles[0][0].id, arretes_eligibles[0][1].id])
            deja_vu.append(arretes_eligibles[0][1])
            non_vu.remove(arretes_eligibles[0][1].id)
        else:
            return aretes
    return aretes

def mettre_a_jour_deja_vu(deja_vu: List[List[Station]], current: [Station, Station], aretes: [[int, int]]) -> None:
    station_a = current[0]
    station_b = current[1]
    index_a = None
    index_b = None

    # Trouver les sous-listes contenant les stations
    for idx, sous_liste in enumerate(deja_vu):
        if station_a in sous_liste:
            index_a = idx
        if station_b in sous_liste:
            index_b = idx

    # Cas 1 : Aucune station n'est dans deja_vu
    if index_a is None and index_b is None:
        deja_vu.append([station_a, station_b])
        aretes.append([current[0].id, current[1].id])

    # Cas 2 : Une seule station est dans deja_vu
    elif index_a is not None and index_b is None:
        deja_vu[index_a].append(station_b)
        aretes.append([current[0].id, current[1].id])
    elif index_a is None and index_b is not None:
        deja_vu[index_b].append(station_a)
        aretes.append([current[0].id, current[1].id])

    # Cas 3 : Les deux stations sont dans des sous-listes différentes
    elif index_a is not None and index_b is not None and index_a != index_b:
        # Fusionner les deux sous-listes
        deja_vu[index_a].extend(deja_vu[index_b])
        del deja_vu[index_b]
        aretes.append([current[0].id, current[1].id])

    # Cas 4 : Les deux stations sont déjà dans la même sous-liste
    # Rien à faire dans ce cas

def kruskal():
    deja_vu: List[List[Station]] = []
    aretes: [[int, int]] = []

    aretes_eligibles: List[Tuple[Station, Station, int]] = []

    for station in all_stations:
        for voisin in station.voisins:
            aretes_eligibles.append((station, voisin[0], voisin[1]))

    # Trier les arêtes par poids (le dernier élément du tuple)
    aretes_eligibles.sort(key=lambda x: x[2])

    while len(aretes_eligibles) > 0:
        current_arete = [aretes_eligibles[0][0], aretes_eligibles[0][1]]
        mettre_a_jour_deja_vu(deja_vu, current_arete, aretes)
        del aretes_eligibles[0]

    return aretes

def create_data():
    # Chemin du fichier
    file_path = "../Data/metro.txt"

    stations = []
    can_add_station = False
    can_add_edge = False
    # Lecture et traitement des lignes
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()  # Supprimer les espaces inutiles au début/fin
                if line.startswith("V"):
                    if can_add_station:
                        # Action à effectuer si la ligne commence par "V"
                        parts = line.split(" ;")
                        sub_parts = parts[0].split(" ", 2)
                        sub_parts2 = parts[2].split(" ")

                        id_station = sub_parts[1]
                        name_station = sub_parts[2]
                        lignes_station = {parts[1]: sub_parts2[1]}
                        is_terminus_station = sub_parts2[0].lower() == "true"

                        stations.append(Station(int(id_station), name_station, lignes_station, is_terminus_station, []))
                    can_add_station = True
                if line.startswith("E"):
                    if can_add_edge:
                        parts = line.split(" ")
                        station_1 = get_station_by_id(int(parts[1]), stations)
                        station_2 = get_station_by_id(int(parts[2]), stations)
                        station_1.voisins.append((station_2, int(parts[3])))
                        station_2.voisins.append((station_1, int(parts[3])))
                    can_add_edge = True
        return stations

    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    except Exception as e:
        print(f"Erreur : {e}")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/dijkstra', methods=['GET'])
def execute_dijkstra():
    # Récupérer les paramètres 's1' et 's2' depuis l'URL
    depart = int(request.args.get('s1'))
    arrivee = int(request.args.get('s2'))

    premiere_station = get_station_by_id(depart, all_stations)
    derniere_station = get_station_by_id(arrivee, all_stations)
    dijkstra_test = dijkstra(premiere_station, derniere_station)

    if dijkstra_test is None:
        print("Error")
        response = {
            "status": "400"
        }
    else:
        choix_l = choix_lignes(dijkstra_test, derniere_station.id)
        sommets = [(choix_l[i][0], int(choix_l[i+1][0])) for i in range(len(choix_l)-1)]
        sommets_ordonne = sommets
        sommets_ordonne.reverse()
        itineraire = get_full_itineraire(choix_l, dijkstra_test[derniere_station.id][1])

        response = {
            "status": 200,
            "data": {
                "stations": sommets_ordonne,
                "itineraire": itineraire,
                "temps": dijkstra_test[derniere_station.id][1]
            }
        }

    # Retourner une réponse JSON
    return jsonify(response)

@app.route('/prim', methods=['GET'])
def execute_prim():
    depart = int(request.args.get('depart'))
    depart_station = get_station_by_id(depart, all_stations)
    aretes = prim(depart_station)

    response = {
        "status": 200,
        "data": {
            "aretes": aretes
        }
    }

    return jsonify(response)

@app.route('/kruskal', methods=['GET'])
def execute_kruskal():
    aretes = kruskal()

    response = {
        "status": 200,
        "data": {
            "aretes": aretes
        }
    }

    return jsonify(response)

all_stations = create_data()
# creer connexite
creer_connexite()
print("ready")

if __name__ == '__main__':
    app.run(debug=True)
