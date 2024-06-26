#view.py
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from api.google_maps_link_gen import create_google_maps_link, create_google_maps_link_for_combination,generate_google_maps_link

from api.models import Route

from .mapping_utils import find_routes_combination, find_routes_with_common_midway
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

        serialized_results = [{'id': route.id, 'location': route.location, 'destination': route.destination, 'description': route.description, 'ride_fee': route.ride_fee,'google_maps_link':route.google_maps_link} for route in results]
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

    start_route, end_route, common_midway_stations = find_routes_with_common_midway(start_location, end_destination)

    if start_route and end_route and common_midway_stations:
        common_midway_station = common_midway_stations[0]  # Access the first element of the list

        data = {
            'start_route': {
                'id': start_route.id,
                'location': start_route.location,
                'destination': start_route.destination,
                'google_maps_link': generate_google_maps_link(start_route),
            },
            'end_route': {
                'id': end_route.id,
                'location': end_route.location,
                'destination': end_route.destination,
                'google_maps_link': generate_google_maps_link(end_route),
            },
            'common_midway_station': {
                'id': common_midway_station.id,
                'name': common_midway_station.name
            },
        }
        
        # Create the Google Maps link using the combined midway stations
        origin = start_location
        destination = end_destination
        google_maps_link = create_google_maps_link(start_route.midway_stations.all(), end_route.midway_stations.all(),
                                                   origin, destination, common_midway_station)
        data['google_maps_link'] = google_maps_link
        
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'No common midway station found.'}, status=404)

    
#safe 100%


@require_GET
def find_routes_combination_view(request):
    start_location = request.GET.get('start_location')
    end_destination = request.GET.get('end_destination')

    if not start_location or not end_destination:
        return JsonResponse({'error': 'Both start_location and end_destination parameters are required.'}, status=400)

    combination_routes = find_routes_combination(start_location, end_destination)

    if combination_routes:
        data = {
            'combination_routes': [
                {
                    'id': route.id,
                    'location': route.location,
                    'destination': route.destination,
                    'google_maps_link': generate_google_maps_link(route),
                }
                for route in combination_routes
            ]
        }

        # Create the Google Maps link for the combination of routes
        google_maps_link = create_google_maps_link_for_combination(combination_routes, start_location, end_destination)
        data['google_maps_link'] = google_maps_link

        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'No combination of routes found.'}, status=404)
