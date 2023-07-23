from django.urls import path
from django.views.generic import TemplateView
from .views import RouteDetail, RouteList, search_locations

urlpatterns = [
    path('routes/search/',search_locations, name='search-locations'),
    path('routes/', RouteList.as_view(), name='route-list'),
    path('routes/<int:pk>', RouteDetail.as_view(),name= 'route-detail'),
    path('', TemplateView.as_view(template_name= 'landing-page.html'))
]
