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

    midway_stations = models.ManyToManyField(MidwayStation, related_name='routes')
    def __str__(self):
        return f'Route from {self.location} to {self.destination}'
    
