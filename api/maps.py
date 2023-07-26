import urllib.parse

def generate_google_maps_link(data):
    origin = data["shortest_path"][0]
    waypoints = [waypoint["name"] for waypoint in data["switch_stations"]]
    destination = data["shortest_path"][-1]

    # Encode the location names to be used in the URL
    origin_encoded = urllib.parse.quote(origin)

    if waypoints:
        waypoints_encoded = "/".join(urllib.parse.quote(waypoint) for waypoint in waypoints)
    else:
        # If no switch stations, use all the values in shortest_path as waypoints
        waypoints_encoded = "/".join(urllib.parse.quote(location) for location in data["shortest_path"][1:-1])

    destination_encoded = urllib.parse.quote(destination)

    # Construct the Google Maps URL
    google_maps_link = f"https://www.google.com/maps/dir/{origin_encoded}/{waypoints_encoded}/{destination_encoded}/"

    return google_maps_link
