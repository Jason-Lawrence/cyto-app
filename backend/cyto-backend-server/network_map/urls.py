""""""
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('network-maps', views.NetworkMapViewSet)
nested = routers.NestedDefaultRouter(router, r'network-maps', lookup='network_map')
nested.register('nodes', views.NodeViewSet)

app_name = 'network_map'

urlpatters = [
    path('', include(router.urls)),
    path('', include(nested.urls))
]
