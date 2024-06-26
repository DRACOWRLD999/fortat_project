def create_google_maps_link(start_midway_stations, end_midway_stations, origin, destination, common_midway_station):
    # Find the combined list of midway stations, considering the common midway station
    combined_midway_stations = []
    for station in start_midway_stations:
        if station != common_midway_station:
            combined_midway_stations.append(station.name)  # Extract the name of the midway station
        else:
            break

    for station in end_midway_stations:
        combined_midway_stations.append(station.name)  # Extract the name of the midway station

    # Encode the origin, destination, and combined midway stations for the Google Maps link
    origin_encoded = origin.replace(" ", "+")
    destination_encoded = destination.replace(" ", "+")
    midway_stations_encoded = "|".join([station.replace(" ", "+") for station in combined_midway_stations])

    # Create the Google Maps link
    google_maps_link = f"https://www.google.com/maps/dir/?api=1&origin={origin_encoded}&destination={destination_encoded}&waypoints={midway_stations_encoded}&region=iq"
    
    return google_maps_link





def create_google_maps_link_for_combination(routes_with_midway_stations, start_location, end_destination):
    waypoints = []
    origin = start_location.replace(" ", "+")
    destination = end_destination.replace(" ", "+")
    waypoints.append(origin)

    routes_with_midway_stations = routes_with_midway_stations[1:]

    for route in routes_with_midway_stations:
        midway_stations = [station.name.replace(" ", "+") for station in route.midway_stations.all()]
        waypoints.extend(midway_stations)

    waypoints_str = "|".join(waypoints)
    google_maps_link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints_str}&region=iq"

    return google_maps_link

def generate_google_maps_link(route):
    origin = route.location.replace(" ", "+")
    destination = route.destination.replace(" ", "+")
    
    midway_stations = [station.name.replace(" ", "+") for station in route.midway_stations.all()]
    if midway_stations:
        waypoints = "|".join(midway_stations)
        google_maps_link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}&region=iq"
    else:
        google_maps_link = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&region=iq"
    
    return google_maps_link
