from api.models import Route

from api.models import Route

def find_routes_with_common_midway(start_location, end_destination):

    start_routes = Route.objects.filter(location=start_location)
    end_routes = Route.objects.filter(destination=end_destination)
    
    
    # Collect midway stations for both sets of routes
    start_midway_stations = set()
    end_midway_stations = set()
    for route in start_routes:
        start_midway_stations.update(route.midway_stations.all())
    for route in end_routes:
        end_midway_stations.update(route.midway_stations.all())
        
        
        
    # Find common midway stations between start and end routes
    common_midway_stations = start_midway_stations.intersection(end_midway_stations)
    if common_midway_stations:
        start_routes = start_routes.filter(midway_stations__in=common_midway_stations)
        end_routes = end_routes.filter(midway_stations__in=common_midway_stations)

        return start_routes.first(), end_routes.first(), list(common_midway_stations)
    else:
        return None, None, None


#safe 100%



def find_routes_combination(start_location, end_destination, visited_routes=None):
    if visited_routes is None:
        visited_routes = set()

    direct_route = Route.objects.filter(location=start_location, destination=end_destination).first()
    if direct_route:
        return [direct_route]

    if start_location in visited_routes:
        return None

    visited_routes.add(start_location)

    routes_from_start = Route.objects.filter(location=start_location)

    # Check each route for a possible combination
    for route in routes_from_start:
        combination = find_routes_combination(route.destination, end_destination, visited_routes)

        if combination:
            return [route] + combination

