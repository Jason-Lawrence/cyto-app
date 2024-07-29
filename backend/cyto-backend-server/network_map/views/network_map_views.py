"""
Views for the Network Map API.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication

from .. import models, serializers


class NetworkMapViewSet(viewsets.ModelViewSet):
    """View for CRUD operations on Network Maps."""
    serializer_class = serializers.NetworkMapDetailSerializer
    queryset = models.NetworkMap.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True)
    def cytoscape(self, request, pk=None):
        """Return the Network Map data in cytoscape format."""
        network_map =  self.get_object()
        nodes = models.Node.objects.filter(network_map=network_map)
        edges = models.Edge.objects.filter(network_map=network_map)

        node_elements = [
            {
                'group': 'nodes',
                'data': {
                    'id': node.nid,
                    'label': node.label,
                    'parent': node.parent
                },
                'position': {
                    'x': node.x,
                    'y': node.y
                },
                'selectable': node.selectable,
                'locked': node.locked,
                'grabbable': node.grabbable,
                'classes': node.classes,
                'style': node.style,
                'scratch': node.scratch
            }
        for node in nodes]

        edge_elements = [
            {
                'group': 'edges',
                'data': {
                    'id': edge.eid,
                    'label': edge.label,
                    'source': edge.source.nid,
                    'target': edge.target.nid
                },
                'pannable': edge.pannable
            }
        for edge in edges]

        elements = node_elements + edge_elements

        cytoscape_data = {
            'elements': elements,
            'layout': network_map.layout
        }

        return Response(cytoscape_data, status=status.HTTP_200_OK)
    
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
