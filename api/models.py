#models.py
from django.core.validators import RegexValidator
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

    google_maps_link = models.URLField(max_length=10000, default='https://www.google.com/maps')

    midway_stations = models.ManyToManyField(MidwayStation, related_name='routes')  # Use related_name

    def __str__(self):
        return f'Route from {self.location} to {self.destination}'
    
    def initialize_google_maps_link(self):
        origin = self.location.replace(" ", "+")
        destination = self.destination.replace(" ", "+")
        midway_stations = "|".join([station.name.replace(" ", "+") for station in self.midway_stations.all()])

        self.google_maps_link = f"https://www.google.com/maps/dir/{origin}/{midway_stations}/{destination}/"

    def save(self, *args, **kwargs):
        # Initialize the Google Maps link before saving the object
        self.initialize_google_maps_link()
        super().save(*args, **kwargs)