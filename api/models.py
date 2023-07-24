from queue import PriorityQueue

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Prefetch

arabic_and_english_letters_validator = RegexValidator(
    r'^[a-zA-Z\u0600-\u06FF\s]+$',
    'Only Arabic and English letters are allowed.'
)

class MidwayStation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Route(models.Model):
    location = models.CharField(
        max_length=100,
        validators=[arabic_and_english_letters_validator]
    )
    destination = models.CharField(
        max_length=100,
        validators=[arabic_and_english_letters_validator]
    )
    description = models.TextField(blank=True, null=True)

    ride_fee = models.DecimalField(max_digits=5, decimal_places=0)

    google_maps_link = models.URLField(max_length=10000, default='https://www.google.com/maps')

    midway_stations = models.ManyToManyField(MidwayStation, related_name='routes')  # Use related_name

    def __str__(self):
        return f'Route from {self.location} to {self.destination}'


    @classmethod
    def a_star_shortest_path(cls, start_location, end_destination):
        pq = PriorityQueue()
        pq.put((0, start_location, [start_location]))  # (total_cost, current_location, path)

        visited = set()

        while not pq.empty():
            total_cost, current_location, path = pq.get()

            if current_location == end_destination:
                return total_cost, path

            if current_location not in visited:
                visited.add(current_location)

                # Get the Route objects associated with the current location
                current_routes = cls.objects.filter(location=current_location)

                for route in current_routes:
                    next_location = route.destination
                    next_cost = total_cost + route.ride_fee
                    next_path = path + [next_location]

                    priority = next_cost

                    pq.put((next_cost, next_location, next_path))

        raise ValueError(f"No path found between {start_location} and {end_destination}")

    def __str__(self):
        return f'Route from {self.location} to {self.destination}'
