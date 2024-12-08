from graphe import Station

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

all_stations = [arret3_1, arret3_2, arret3_4, arret71_84_1, arret3_71_84, arret71_84_3, arret71_84_4,
                arret71_84_5, arret71_84_6, arret35_1, arret35_2, arret35_3]
