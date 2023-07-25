from django.urls import path
from django.views.generic import TemplateView
from .views import (
      NotFoundView, RouteDetail, RouteList,  find_multiple_routes_to_destination, find_routes_with_switch_station_view, search_locations,
)

urlpatterns = [
    path('routes/search/', search_locations, name='search-locations'),
    path('routes/', RouteList.as_view(), name='route-list'),
    path('routes/<int:pk>/', RouteDetail.as_view(), name='route-detail'),
    path('routes/combined_routes/', find_multiple_routes_to_destination, name='multiple-routes-to-destination'),
    path('routes/midway_switch_routes/', find_routes_with_switch_station_view, name='routes-with-switch-station'),    path('', TemplateView.as_view(template_name='landing-page.html')),
    path('<path:not_found>/', NotFoundView.as_view(), name='not-found'),
]
