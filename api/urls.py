#url.py
from django.urls import path
from django.views.generic import TemplateView
from .views import (
      NotFoundView, RouteDetail, RouteList, search_locations
)
from api import views

urlpatterns = [
    path('find_common_midway/', views.find_common_midway_station, name='find-common-midway'),
    path('find_routes_combination/', views.find_routes_combination_view, name='find-routes-combination'),
    path('routes/search/',search_locations, name='search-locations'),
    path('routes/', RouteList.as_view(), name='route-list'),
    path('routes/<int:pk>', RouteDetail.as_view(),name= 'route-detail'),
    path('', TemplateView.as_view(template_name= 'landing-page.html')),
    path('<path:not_found>/', NotFoundView.as_view(), name='not-found'),
]
