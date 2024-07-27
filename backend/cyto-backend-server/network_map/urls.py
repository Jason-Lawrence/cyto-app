""""""
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('network-maps', views.NetworkMapViewSet)

app_name = 'network_map'

urlpatters = [
    path('', include(router.urls))
]
