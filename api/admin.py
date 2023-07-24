
from django.contrib import admin
from .models import MidwayStation, Route

class RouteAdmin(admin.ModelAdmin):
    filter_horizontal = ['midway_stations']
    
    
admin.site.register(Route, RouteAdmin)
admin.site.register(MidwayStation)