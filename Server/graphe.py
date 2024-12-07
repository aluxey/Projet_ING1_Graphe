from dataclasses import dataclass
from typing import List, Dict, Tuple

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


def get_station_by_id(station_id):
    for station in all_stations:
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
    # print(f"de {first_station.name} vers {last_station.name}")
    terminus = set()
    calcul_direction([], terminus, first_station, last_station, ligne, False, first_station.lignes[ligne])
    return terminus


def get_ligne_optimale(dijkstra: {int: Tuple[int, int]}, initial: Station):
    current = initial
    lst_lignes = set(current.lignes.keys())
    while len(lst_lignes) != 0 or len(lst_lignes) != 1:
        current = get_station_by_id(dijkstra[current.id][0])
        lst_lignes_suivantes = lst_lignes & current.lignes.keys()
        if len(lst_lignes_suivantes) == 1:
            return next(iter(lst_lignes_suivantes)) # taille 1, donc le seul élément
        if len(lst_lignes_suivantes) == 0:
            return next(iter(lst_lignes)) # n'importe laquelle des lignes
        lst_lignes = lst_lignes_suivantes
    if len(lst_lignes) == 1:
        return lst_lignes[0]
    if len(lst_lignes) == 0:
        return None #


def choix_lignes(dijkstra: {int: Tuple[int, int]}, arrivee: int):
    ligne_choisie: str = None
    ligne_par_arret: [(int, str)] = []
    current = get_station_by_id(arrivee)
    ligne_par_arret.append((current.id, get_ligne_optimale(dijkstra, current)))
    while current.id in dijkstra:
        x = get_station_by_id(dijkstra[current.id][0])
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
    if get_station_by_id(init).lignes[ligne] == get_station_by_id(next).lignes[ligne]:
        return False

    # si on est initialement sur le branchement 0
    if get_station_by_id(init).lignes[ligne] == "0":
        return False

    # si on arrive sur le branchement 0
    if get_station_by_id(next).lignes[ligne] == "0":
        return False

    # si on arrive sur un autre branchement que 0 et qu'on vient d'un autre branchement que 0
    print(f"je doit changer de direction pour aller de {init} à {next}")
    return True




def trier_choix_lignes(choix_l: [(int, str)], temps: int):
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
    print(f"Débutez à la station {get_station_by_id(init[0]).name}")
    while not est_fini:
        if next[1] == init[1] or next[1].startswith(init[1] + "-"): # on peut rester sur la meme ligne
            # print("garde la meme ligne")
            if doit_changer_direction(init[0], next[0], ligne):
                # print("changement...")
                print(f"Prenez la ligne {ligne} direction {" ou ".join(get_all_possible_destinations(get_station_by_id(init[0]), get_station_by_id(fin[0]), ligne))} jusqu'à {get_station_by_id(fin[0]).name}")
                # print("...changement")
                init = fin
            fin = next
            if next[1].startswith(init[1] + "-"):
                doit_marcher = True
        else: # changement de ligne
            # print("change de ligne")
            if doit_marcher:
                print(f"Prenez la ligne {ligne} direction {" ou ".join(get_all_possible_destinations(get_station_by_id(init[0]), get_station_by_id(fin[0]), ligne))} jusqu'à {get_station_by_id(fin[0]).name}")
                print(f"Marchez jusqu'à la station {get_station_by_id(next[0]).name}")
            else:
                print(f"Prenez la ligne {ligne} direction {" ou ".join(get_all_possible_destinations(get_station_by_id(init[0]), get_station_by_id(fin[0]), ligne))} jusqu'à {get_station_by_id(next[0]).name}")
            affiche_indication = True
            init = next
            ligne = init[1].split("-", 1)[0]
            doit_marcher = False
        if index_parcours == (len(choix_lignes) - 1): # si on est sur le dernier sommet
            if not affiche_indication:
                print(f"Prenez la ligne {ligne} direction {" ou ".join(get_all_possible_destinations(get_station_by_id(init[0]), get_station_by_id(fin[0]), ligne))} jusqu'à {get_station_by_id(next[0]).name}")
            print(f"Vous devriez arriver à {get_station_by_id(next[0]).name} en {temps} minutes")
            est_fini = True
        else:
            affiche_indication = False
            index_parcours += 1
            next = choix_lignes[index_parcours]


# if __name__ == "__main__":
#     main()


quinconces: Station = Station(1, "quinconces", {"3": "0"}, True, [])
mairie: Station = Station(2, "mairie", {"3": "0"}, False, [])
republique: Station = Station(3, "republique", {"3": "0"}, False, [])
eglise: Station = Station(4, "eglise", {"3": "2"}, False, [])
issac: Station = Station(5, "issac", {"3": "2"}, True, [])
zola: Station = Station(6, "zola", {"3": "1"}, False, [])
lycee: Station = Station(7, "lycee", {"3": "1", "84": "0"}, False, [])
villepreux: Station = Station(8, "villepreux", {"3": "1"}, True, [])
proust: Station = Station(9, "proust", {"84": "0"}, True, [])
cantinole: Station = Station(10, "cantinole", {"84": "0"}, False, [])
aulnes: Station = Station(11, "aulnes", {"84": "2"}, False, [])
rostand: Station = Station(12, "rostand", {"84": "2"}, True, [])
cinq_chemins: Station = Station(13, "5 chemins", {"84": "1"}, False, [])
aeroport: Station = Station(14, "aeroport", {"84": "1"}, True, [])

quinconces.voisins.append((mairie, 2))
mairie.voisins.append((quinconces, 2))
mairie.voisins.append((republique, 3))
republique.voisins.append((mairie, 3))
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
cantinole.voisins.append((aulnes, 3))
cantinole.voisins.append((cinq_chemins, 3))
aulnes.voisins.append((cantinole, 3))
aulnes.voisins.append((rostand, 2))
rostand.voisins.append((aulnes, 2))
cinq_chemins.voisins.append((cantinole, 3))
cinq_chemins.voisins.append((aeroport, 2))
aeroport.voisins.append((cinq_chemins, 2))



arret3_1: Station = Station(1, "TERM 3 - 1", {"3": "0"}, True, [])
arret3_2: Station = Station(2, "arret 3 - 2", {"3": "0"}, False, [])
arret3_4: Station = Station(4, "TERM 3 - 4", {"3": "0"}, True, [])

arret71_84_1: Station = Station(5, "TERM 71 - 1", {"71": "0", "84": "0"}, True, [])
arret3_71_84: Station = Station(6, "arret 3 / 71 / 84 - 2", {"71": "0", "3": "0", "84": "0"}, False, [])
arret71_84_3: Station = Station(7, "arret 71 / 84 - 3", {"71": "0", "84": "0"}, False, [])
arret71_84_4: Station = Station(8, "arret 71 / 84 - 4", {"71": "0", "84": "0"}, False, [])
arret71_84_5: Station = Station(9, "arret 71 / 84 - 5", {"71": "0", "84": "0"}, True, [])
arret71_84_6: Station = Station(10, "TERM 71 / 84 - 6", {"84": "0"}, True, [])

arret35_1: Station = Station(17, "TERM 35 - 1", {"35": "0"}, True, [])
arret35_2: Station = Station(18, "arret 35 - 2", {"35": "0"}, False, [])
arret35_3: Station = Station(19, "TERM 35 - 3", {"35": "0"}, True, [])

arret3_1.voisins.append((arret3_2, 1))
arret3_2.voisins.append((arret3_1, 1))
arret3_2.voisins.append((arret3_71_84, 1))
arret3_4.voisins.append((arret3_71_84, 1))

arret71_84_1.voisins.append((arret3_71_84, 1))
arret3_71_84.voisins.append((arret71_84_1, 1))
arret3_71_84.voisins.append((arret71_84_3, 1))
arret3_71_84.voisins.append((arret3_2, 1))
arret3_71_84.voisins.append((arret3_4, 1))
arret71_84_3.voisins.append((arret3_71_84, 1))
arret71_84_3.voisins.append((arret71_84_4, 1))
arret71_84_4.voisins.append((arret71_84_3, 1))
arret71_84_4.voisins.append((arret71_84_5, 1))
arret71_84_5.voisins.append((arret71_84_4, 1))
arret71_84_5.voisins.append((arret71_84_6, 1))
arret71_84_6.voisins.append((arret71_84_5, 1))
arret71_84_6.voisins.append((arret35_1, 1))

arret35_1.voisins.append((arret71_84_6, 1))
arret35_1.voisins.append((arret35_2, 1))
arret35_2.voisins.append((arret35_1, 1))
arret35_2.voisins.append((arret35_3, 1))
arret35_3.voisins.append((arret35_2, 1))

all_stations = [quinconces, mairie, republique, eglise, issac, zola, lycee, villepreux, proust,
                cantinole, aulnes, rostand, cinq_chemins, aeroport]
# all_stations = [arret3_1, arret3_2, arret3_4, arret71_84_1, arret3_71_84, arret71_84_3, arret71_84_4,
#                 arret71_84_5, arret71_84_6, arret35_1, arret35_2, arret35_3]



premiere_station = mairie
derniere_station = cantinole
dijkstra_test = dijkstra(premiere_station, derniere_station)
print(premiere_station.name + " -> " + derniere_station.name)
if dijkstra_test is None:
    print("Probleme")
else:
    choix_l = choix_lignes(dijkstra_test, derniere_station.id)
    print(choix_l)
    trier_choix_lignes(choix_l, dijkstra_test[derniere_station.id][1])

print()