from api.models import Route

def switch_station(route1: Route, route2: Route):
    # Get the midway stations of each route
    midway_stations1 = route1.midway_stations.all()
    midway_stations2 = route2.midway_stations.all()

    # Find the mutual stations by taking the intersection of the two sets
    mutual_stations = midway_stations1.intersection(midway_stations2)

    return list(mutual_stations)
