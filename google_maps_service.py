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
            origin_coordinates = data["routes"][0]["legs"][0]["start_location"]
            destination_coordinates = data["routes"][0]["legs"][0]["end_location"]
            return distance, origin_coordinates, destination_coordinates
        else:
            return None, "No route found"
    else:
        return None, "Error: " + response.status_code


## generate weights between each pair of addresses where the weight is the distance between the two addresses

def get_address_distances_and_coordinates(addresses):
    weights = {}
    coordinates = {}
    for i in range(len(addresses)):
        for j in range(i+1, len(addresses)):
            origin = addresses[i]
            destination = addresses[j]
            distance, origin_coordinates, destination_coordinates = get_distance(origin, destination)
            if distance:
                distance_value = float(distance.split(" ")[0])
                weights[(origin, destination)] = distance_value
            ## add coordinates if not already added
            if origin not in coordinates:
                coordinates[origin] = origin_coordinates
            if destination not in coordinates:
                coordinates[destination] = destination_coordinates


    return weights, coordinates
