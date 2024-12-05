import json
from pathlib import Path

def clean_station_name(name):
    """Nettoie les noms des stations pour les correspondances."""
    return name.replace("@", " ").strip()

def merge_data(stations_file, positions_file, output_file):
    # Charger les fichiers JSON
    with open(stations_file, 'r', encoding='utf-8') as sf, open(positions_file, 'r', encoding='utf-8') as pf:
        stations_data = json.load(sf)
        positions_data = json.load(pf)

    # Créer un dictionnaire pour les positions
    positions_map = {
        clean_station_name(pos["nom_station"]): {"posX": pos["posX"], "posY": pos["posY"]}
        for pos in positions_data["positions"]
    }

    # Ajouter les positions aux stations
    for station in stations_data["stations"]:
        station_name = clean_station_name(station["name"])
        if station_name in positions_map:
            station.update(positions_map[station_name])
        else:
            station["posX"] = None
            station["posY"] = None

    # Sauvegarder les données fusionnées
    with open(output_file, 'w', encoding='utf-8') as of:
        json.dump(stations_data, of, ensure_ascii=False, indent=4)
    print(f"Fichier fusionné sauvegardé sous {output_file}")

# Chemins des fichiers
stations_file = "sorted_metro.json"  # Remplacez par le chemin de votre fichier
positions_file = "pospoints.json"  # Remplacez par le chemin de votre fichier
output_file = "Data/merged_data.json"

# Exécuter la fusion
merge_data(stations_file, positions_file, output_file)
