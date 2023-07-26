#view.py
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Route

from .mapping_utils import find_routes_with_common_midway
from .models import Route
from .permissions import IsAdminOrReadOnly
from .serializers import RouteSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
@method_decorator(cache_page(15*60), name='dispatch')
class RouteList(generics.ListCreateAPIView):
    serializer_class = RouteSerializer
    pagination_class = CustomPagination
    queryset = Route.objects.all()
    permission_classes = [IsAdminOrReadOnly]


@method_decorator(cache_page(15*60), name='dispatch')
class RouteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    permission_classes = [IsAdminOrReadOnly]

def search_locations(request):
    if 'query' in request.GET:
        query = request.GET['query']

        #search for similar matches in location or destination
        location_results = Route.objects.filter(location__icontains=query)[:10]
        destination_results = Route.objects.filter(destination__icontains=query)[:10]

        # If there are no results in both location and destination then search in description
        if not location_results and not destination_results:
            description_results = Route.objects.filter(description__icontains=query)[:10]
            results = description_results
        else:
            results = location_results | destination_results

        serialized_results = [{'id': route.id, 'location': route.location, 'destination': route.destination, 'description': route.description, 'ride_fee': route.ride_fee} for route in results]
        return JsonResponse(serialized_results, safe=False)
    return JsonResponse([], safe=False)


def find_routes_with_no_straight_route(start_location, destination):
    def find_routes_helper(current_location, target_location, used_routes, total_cost):
        if current_location == target_location:
            return [(used_routes, total_cost)]
        
        routes_from_current_location = Route.objects.filter(location=current_location)
        valid_routes = []
        
        for route in routes_from_current_location:
            if route.destination in used_routes:
                continue
            new_used_routes = used_routes + [route.destination]
            new_total_cost = total_cost + route.ride_fee
            results = find_routes_helper(route.destination, target_location, new_used_routes, new_total_cost)
            valid_routes.extend(results)
        
        return valid_routes

    routes_combinations = find_routes_helper(start_location, destination, [start_location], 0)
    return routes_combinations

# In views.py
def find_multiple_routes_to_destination(request):
    if 'start_location' in request.GET and 'destination' in request.GET:
        start_location = request.GET['start_location']
        destination = request.GET['destination']

        routes_combinations = find_routes_with_no_straight_route(start_location, destination)

        serialized_results = [{'routes': [route for route in routes], 'total_cost': cost} for routes, cost in routes_combinations]
        return JsonResponse(serialized_results, safe=False)

    return JsonResponse([], safe=False)


class NotFoundView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)



@require_GET
def find_common_midway_station(request):
    start_location = request.GET.get('start_location')
    end_destination = request.GET.get('end_destination')

    if not start_location or not end_destination:
        return JsonResponse({'error': 'Both start_location and end_destination parameters are required.'}, status=400)

    start_route, end_route, common_midway_list = find_routes_with_common_midway(start_location, end_destination)

    if start_route and end_route and common_midway_list:
        data = {
            'start_route': {
                'id': start_route.id,
                'location': start_route.location,
                'destination': start_route.destination,
            },
            'end_route': {
                'id': end_route.id,
                'location': end_route.location,
                'destination': end_route.destination,
            },
            'common_midway_stations': [
                {'id': midway_station.id, 'name': midway_station.name} for midway_station in common_midway_list
            ],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'No common midway station found.'}, status=404)
    
#safe 100%
