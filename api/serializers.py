from rest_framework import serializers

from .models import MidwayStation, Route

from rest_framework import serializers
from .models import Route, MidwayStation

class MidwayStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidwayStation
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    midway_stations = serializers.PrimaryKeyRelatedField(queryset=MidwayStation.objects.all(), many=True)

    class Meta:
        model = Route
        fields = '__all__'
