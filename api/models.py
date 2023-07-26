<<<<<<< HEAD
#models.py
from django.core.validators import RegexValidator
=======
>>>>>>> 15c98ac5c214b391b2584c9f20296889595a9797
from django.db import models


class MidwayStation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Route(models.Model):
    location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    ride_fee = models.DecimalField(max_digits=5, decimal_places=0)
    google_maps_link = models.URLField(max_length=10000, default='')

<<<<<<< HEAD
    google_maps_link = models.URLField(max_length=10000, default='https://www.google.com/maps')

    midway_stations = models.ManyToManyField(MidwayStation, related_name='routes')  # Use related_name

    def __str__(self):
        return f'Route from {self.location} to {self.destination}'
=======
    # Update the Route model to include midway stations
    midway_stations = models.ManyToManyField(MidwayStation, related_name='routes')

    def __str__(self):
        return f'Route from {self.location} to {self.destination}'
    
def find_routes_with_multiple_hops(start_location, destination):
    routes = []
    for route in Route.objects.filter(start_location=start_location):
        if route.destination != destination:
            next_route = find_routes_with_multiple_hops(route.destination, destination)
            if next_route:
                routes.append({
                    'route': route,
                    'next_route': next_route,
                    'total_cost': route.ride_fee + next_route['total_cost']
                })
        else:
            routes.append({
                'route': route,
                'total_cost': route.ride_fee
            })
    return routes
>>>>>>> 15c98ac5c214b391b2584c9f20296889595a9797
