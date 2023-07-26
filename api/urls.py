#url.py
from django.urls import path
from django.views.generic import TemplateView
from .views import (
      NotFoundView, RouteDetail, RouteList,  find_multiple_routes_to_destination, find_routes_with_switch_station_view, search_locations,
)

urlpatterns = [
<<<<<<< HEAD
    path('find_common_midway/', views.find_common_midway_station, name='find-common-midway'),
    path('routes/search/',search_locations, name='search-locations'),
    path('routes/', RouteList.as_view(), name='route-list'),
    path('routes/<int:pk>', RouteDetail.as_view(),name= 'route-detail'),
    path('', TemplateView.as_view(template_name= 'landing-page.html')),
=======
    path('routes/search/', search_locations, name='search-locations'),
    path('routes/', RouteList.as_view(), name='route-list'),
    path('routes/<int:pk>/', RouteDetail.as_view(), name='route-detail'),
    path('routes/combined_routes/', find_multiple_routes_to_destination, name='multiple-routes-to-destination'),
    path('routes/midway_switch_routes/', find_routes_with_switch_station_view, name='routes-with-switch-station'),    path('', TemplateView.as_view(template_name='landing-page.html')),
>>>>>>> 15c98ac5c214b391b2584c9f20296889595a9797
    path('<path:not_found>/', NotFoundView.as_view(), name='not-found'),
]
