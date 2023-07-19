from rest_framework import generics
from django.http import JsonResponse
from django.db.models import Q
from .models import Route
from .serializers import RouteSerializer

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10

class RouteList(generics.ListCreateAPIView):
    serializer_class = RouteSerializer
    pagination_class = CustomPagination
    queryset = Route.objects.all()



class RouteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    


def search_locations(request):
    if 'query' in request.GET:
        query = request.GET['query']

        #case-insensitive search for similar matches
        results = Route.objects.filter(Q(location__icontains=query) | Q(destination__icontains=query))[:10]

        # Serialize the results to JSON
        serialized_results = [{'id': route.id, 'location': route.location, 'destination': route.destination, 'description': route.description, 'ride_fee':route.ride_fee} for route in results]
        return JsonResponse(serialized_results, safe=False)
    return JsonResponse([], safe=False)


    
    