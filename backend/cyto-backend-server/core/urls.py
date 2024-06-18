from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from django.urls import path
from . import views

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('health-check/', views.health_check, name='health-check')
]