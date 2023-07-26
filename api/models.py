#models.py
from django.core.validators import RegexValidator
from django.db import models

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