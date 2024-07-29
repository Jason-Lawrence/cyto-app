"""Views for the Node API."""
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .. import models, serializers


class NodeViewSet(viewsets.ModelViewSet):
    """View for CRUD operations on Nodes."""
    serializer_class = serializers.NodeDetailSerializer
    queryset = models.Node.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Get the proper serializer class for the request."""
        if self.action == 'list':
            return serializers.NodeSerializer

        else:
            return self.serializer_class

    def get_queryset(self):
        """Get Nodes belonging to the Network Map."""
        return (
            self.queryset.filter(network_map=self.kwargs['network_map_pk'])
            .order_by('-id')
            .distinct()
        )

    def create(self, request, *args, **kwargs):
        request.data._mutable = True # pylint: disable=protected-access
        request.data['network_map'] = self.kwargs['network_map_pk']
        request.data._mutable = False # pylint: disable=protected-access
        return super().create(request, *args, **kwargs)
