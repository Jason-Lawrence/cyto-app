""""""
from rest_framework import serializers

from .. import models


class NodeSerializer(serializers.ModelSerializer):
    """"""
    parent = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = models.Node
        fields = [
            'id', 'label', 'parent'
        ]
        read_only_fields = ['id']


class NodeDetailSerializer(NodeSerializer):
    """"""
    network_map = serializers.PrimaryKeyRelatedField()

    class Meta(NodeSerializer.Meta):
        fields = (
            NodeSerializer.Meta.fields + [
                'network_map', 'x', 'y', 'selectable',
                'locked', 'grabbable', 'pannable',
                'classes', 'style', 'scratch'
            ]
        )
