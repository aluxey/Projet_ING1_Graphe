# Structures pour stocker les données
stations = {}  # Dictionnaire des stations
edges = []  # Liste des arêtes

# Lire le fichier
with open("metro.txt", "r", encoding="utf-8") as file:
    count = 0

    for line in file:
        line = line.strip()  
        if line.startswith("V"): 
            count = count + 1
        
        elif line.startswith("E"): 
            
            _, start, end, time = line.split()
            edges.append({
                "start": start,
                "end": end,
                "time": int(time) 
            })

# Afficher les données extraites
print("Stations :", stations)
print("Arêtes :", edges)
