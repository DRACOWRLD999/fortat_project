from django.urls import path

from .views import RouteDetail, RouteList, search_locations

urlpatterns = [
    path('routes/search/',search_locations, name='search-locations'),
    path('routes/', RouteList.as_view(), name='route-list'),
    path('routes/<int:pk>', RouteDetail.as_view(),name= 'route-detail'),
]
