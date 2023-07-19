from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Route
from .serializers import RouteSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10

class RouteList(generics.ListCreateAPIView):
    serializer_class = RouteSerializer
    pagination_class = CustomPagination
    queryset = Route.objects.all()



class RouteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    

from django.db.models import Q


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


