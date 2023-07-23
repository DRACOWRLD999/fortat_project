from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

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



class NotFoundView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"error": "Endpoint not found"}, status=status.HTTP_404_NOT_FOUND)

    def head(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
