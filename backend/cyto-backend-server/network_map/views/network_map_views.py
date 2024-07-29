"""
Views for the Network Map API.
"""
from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication

from .. import models, serializers


class NetworkMapViewSet(viewsets.ModelViewSet):
    """View for CRUD operations on Network Maps."""
    serializer_class = serializers.NetworkMapDetailSerializer
    queryset = models.NetworkMap.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Return the proper serializer class for the request."""
        if self.action in ['list', 'create', 'update']:
            return serializers.NetworkMapSerializer

        else:
            return self.serializer_class

    def get_queryset(self):
        """
        Retrieve Network Maps that belong to the user, 
        and ones that are public.
        """
        return (
            self.queryset.filter(Q(is_public=True) | Q(user=self.request.user))
            .order_by('-id')
            .distinct()
        )

    def perform_create(self, serializer):
        """Create the network map."""
        serializer.save(user=self.request.user)
