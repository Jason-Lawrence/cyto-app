"""

"""
from rest_framework import viewsets
from django.db.models import Q

from .. import models, serializers


class NetworkMapViewSet(viewsets.ModelViewSet):
    """"""
    serializer_class = serializers.NetworkMapDetailSerializer
    queryset = models.NetworkMap.objects.all()
    
    def get_serializer_class(self):
        """"""
        if self.action in ['list', 'create', 'update']:
            return serializers.NetworkMapSerializer

        else:
            return self.serializer_class

    def get_queryset(self):
        """"""
        return self.queryset.filter(
            Q(is_public=True) | 
            Q(user=self.request.user)
        ).order_by('-id').distinct()

    def perform_create(self, serializer):
        """"""
        serializer.save(user=self.request.user)
