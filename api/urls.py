from django.urls import path
from .views import RouteList, RouteDetail, search_locations


urlpatterns = [
    path('Routes/', RouteList.as_view(), name='route-list'),
    path('Routes/<int:pk>', RouteDetail.as_view(),name= 'route-detail'),
    path('search/locations/',search_locations, name='search-locations'),
]
