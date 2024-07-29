"""Views for the Edge API."""
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .. import models, serializers


class EdgeViewSet(viewsets.ModelViewSet):
    """Views for CRUD operations on Edges."""
    serializer_class = serializers.EdgeSerializer
    queryset = models.Edge.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get edges belonging to the network map."""
        return (
            self.queryset.filter(network_map=self.kwargs['network_map_pk'])
            .order_by('-id')
            .distinct()
        )

    def create(self, request, *args, **kwargs):
        """Grab network map from the url."""
        request.data._mutable = True # pylint: disable=protected-access
        request.data['network_map'] = self.kwargs['network_map_pk']
        request.data._mutable = False # pylint: disable=protected-access
        return super().create(request, *args, **kwargs)
