""""""
from rest_framework import serializers

from .. import models



class EdgeSerializer(serializers.ModelSerializer):
    """"""
    source = serializers.PrimaryKeyRelatedField(
        queryset=models.Node.objects.all()
    )
    target = serializers.PrimaryKeyRelatedField(
        queryset=models.Node.objects.all()
    )
    network_map = serializers.PrimaryKeyRelatedField(
        queryset=models.NetworkMap.objects.all(),
        required=False
    )
    
    class Meta:
        model = models.Edge
        fields = [
            'id', 'eid', 'network_map','label', 
            'source', 'target', 'pannable'
        ]
        read_only_fields = ['id', 'eid']

    def create(self, validated_data):
        """"""
        edge = models.Edge.objects.create(**validated_data)
        return edge

    def update(self, instance, validated_data):
        """"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance