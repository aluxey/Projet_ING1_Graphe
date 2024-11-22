import json

# Input and output file paths
input_file = 'metro.txt'
output_json = 'sorted_metro.json'

def process_file(input_file):

    stations = []
    edges = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            if not line or line.startswith("#"): 
                continue

            if line.startswith('V'):  
                parts = line.split(' ;')

                desc = parts[0].split(' ', 2)
                num = desc[1]
                name = desc[2]
                numLigne = parts[1]
                detail = parts[2].split(' ', 2)
                estTerminus = detail[0]
                correspondance = detail[1]

                station = {
                        "id": num,
                        "name": name,
                        "ligne": numLigne,
                        "terminus": estTerminus,
                        "branchement": correspondance
                    }
                stations.append(station)

            elif line.startswith('E'):
                try:
                    _, start, end, time = line.split()
                    edges.append({
                        "start": int(start.strip()),
                        "end": int(end.strip()),
                        "time": int(time.strip())
                    })
                except ValueError as e:
                    print(f"Error processing edge line: {line}\n{e}")

    return stations, edges

def save_to_json(stations, edges, output_file):
    stations.sort(key=lambda x: x["name"].lower() if x["name"] else "")
    data = {
        "stations": stations,
        "edges": edges
    }

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data sorted and saved to '{output_file}'")

# Main Execution
if __name__ == "__main__":
    stations, edges = process_file(input_file)
    save_to_json(stations, edges, output_json)
