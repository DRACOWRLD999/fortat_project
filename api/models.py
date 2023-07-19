# models.py
from django.core.validators import RegexValidator
from django.db import models

arabic_and_english_letters_validator = RegexValidator(
    r'^[a-zA-Z\u0600-\u06FF\s]+$',
    'Only Arabic and English letters are allowed.'
)

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

    def __str__(self):
        return f'Route from {self.location} to {self.destination}'
