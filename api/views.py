from queue import PriorityQueue
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.switch_station import switch_station

from .models import Route
from .permissions import IsAdminOrReadOnly
from .serializers import RouteSerializer


from api.models import Route
from queue import PriorityQueue
def find_shortest_path(request):
    if request.method == 'GET':
        start_location = request.GET.get('start_location')
        end_destination = request.GET.get('end_destination')

        if not start_location or not end_destination:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        try:
            # Find optimal path
            total_cost, shortest_path = Route.a_star_shortest_path(start_location, end_destination)

            # Get list of routes for the shortest path
            route_legs = [Route.objects.get(location=loc, destination=next_loc)
                          for loc, next_loc in zip(shortest_path[:-1], shortest_path[1:])]

            switch_stations = set()  # Use a set to avoid duplicates

            for i in range(len(route_legs) - 1):
                mutual_stations = switch_station(route_legs[i], route_legs[i+1])
                switch_stations.update(mutual_stations)

            # Convert switch_stations set to a list of dictionaries
            switch_stations_data = [{'name': station.name, 'id': station.id} for station in switch_stations]

            return JsonResponse({
                'total_cost': total_cost,
                'shortest_path': shortest_path,
                'switch_stations': switch_stations_data
            })

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

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



class NotFoundView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


