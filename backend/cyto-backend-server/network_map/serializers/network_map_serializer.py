""""""
from rest_framework import serializers

from .. import models


class NetworkMapSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = models.NetworkMap
        fields = [
            'id', 'name', 'description',
            'created_at', 'last_updated',
            'is_public'
        ]
        read_only_fields = ['id', 'created_at', 'last_updated']

    def create(self, validated_data):
        """"""
        network_map = models.NetworkMap.objects.create(**validated_data)
        return network_map
    
    def update(self, instance, validated_data):
        """"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance


class NetworkMapDetailSerializer(NetworkMapSerializer):
    """"""
    nodes = None
    edges = None    

    class Meta(NetworkMapSerializer.Meta):
        fields = (NetworkMapSerializer.Meta.fields + 
                  ['layout', 'nodes', 'edges'])
        
        
    