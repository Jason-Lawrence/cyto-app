""""""
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .. import models, serializers


class NodeViewSet(viewsets.ModelViewSet):
    """"""
    serializer_class = serializers.NodeDetailSerializer
    queryset = models.Node.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """"""
        if self.action == 'list':
            return serializers.NodeSerializer

        else:
            return self.serializer_class

    def get_queryset(self):
        """"""
        return (self.queryset.filter(
                network_map=self.kwargs['network_map_pk'])
            .order_by('-id')
            .distinct()
        )

    def create(self, request, *args, **kwargs):
        request.data['network_map'] = self.kwargs['network_map_pk']
        return super().create(request, *args, **kwargs)

