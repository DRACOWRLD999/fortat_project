from api.models import Route

from api.models import Route

def find_routes_with_common_midway(start_location, end_destination):
    # Query routes with start_location as their location

    start_routes = Route.objects.filter(location=start_location)
    print(start_routes)
    # Query routes with end_destination as their destination
    end_routes = Route.objects.filter(destination=end_destination)
    print(end_routes)
    # Collect midway stations for both sets of routes
    start_midway_stations = set()
    end_midway_stations = set()
    print(start_midway_stations)
    print(end_midway_stations)
    for route in start_routes:
        start_midway_stations.update(route.midway_stations.all())
    print(start_midway_stations)
    for route in end_routes:
        end_midway_stations.update(route.midway_stations.all())
    print(end_midway_stations)
    # Find common midway stations between start and end routes
    common_midway_stations = start_midway_stations.intersection(end_midway_stations)
    print(common_midway_stations)
    if common_midway_stations:
        # If common midway station(s) exist, return instances of the routes and the common midway station(s)
        start_routes = start_routes.filter(midway_stations__in=common_midway_stations)
        end_routes = end_routes.filter(midway_stations__in=common_midway_stations)

        # Return the first instance of each route and a list of common midway stations
        return start_routes.first(), end_routes.first(), list(common_midway_stations)
    else:
        # If no common midway station is found, return None for the midway stations
        return None, None, None
