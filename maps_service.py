import os
import requests

api_key = os.getenv("GCP_API_KEY")

def get_distance(origin, destination):
    if not api_key:
        return None, "API key not found"

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            distance = data["routes"][0]["legs"][0]["distance"]["text"]
            duration = data["routes"][0]["legs"][0]["duration"]["text"]
            return distance, duration
        else:
            return None, "No route found"
    else:
        return None, "Error: " + response.status_code


## ten addresses in Berlin
addresses = [
    "Alexanderplatz, Berlin, Germany",
    "Brandenburg Gate, Berlin, Germany",
    "Fernsehturm Berlin, Germany",
    "Potsdamer Platz, Berlin, Germany",
    "Reichstag building, Berlin, Germany",
    "Berlin Wall Memorial, Germany",
    "Checkpoint Charlie, Berlin, Germany",
    "Kurfürstendamm, Berlin, Germany",
    "Berlin Cathedral, Germany",
    "Charlottenburg Palace, Berlin, Germany"
]

## generate weights between each pair of addresses where the weight is the distance between the two addresses

def get_address_distances(addresses):
    weights = {}
    for i in range(len(addresses)):
        for j in range(i+1, len(addresses)):
            origin = addresses[i]
            destination = addresses[j]
            distance, _ = get_distance(origin, destination)
            if distance:
                distance_value = float(distance.split(" ")[0])
                weights[(origin, destination)] = distance_value

    return weights
