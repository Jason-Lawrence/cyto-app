""""""
from rest_framework import serializers

from .. import models


class NodeSerializer(serializers.ModelSerializer):
    """"""
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Node.objects.all(),
        required=False
    )

    class Meta:
        model = models.Node
        fields = [
            'id', 'nid', 'label', 'parent'
        ]
        read_only_fields = ['id', 'nid']

    def create(self, validated_data):
        """"""
        node = models.Node.objects.create(**validated_data)
        return node

    def update(self, instance, validated_data):
        """"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class NodeDetailSerializer(NodeSerializer):
    """"""
    network_map = serializers.PrimaryKeyRelatedField(
        queryset=models.NetworkMap.objects.all(),
        required=False
    )

    class Meta(NodeSerializer.Meta):
        fields = (
            NodeSerializer.Meta.fields + [
                'network_map', 'x', 'y', 'selectable',
                'locked', 'grabbable', 'pannable',
                'classes', 'style', 'scratch'
            ]
        )
