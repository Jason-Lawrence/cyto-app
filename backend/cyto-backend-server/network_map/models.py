"""
Models for the Network Map app.
"""
from django.db import models
from django.conf import settings


class Layout(models.Model):
    """
    """
    name = models.CharField(max_length=50)
    data = models.JSONField(null=True, blank=True)


class NetworkMap(models.Model):
    """
    Model for storing Network Maps.
    
    Args:
        user (:obj: user.User): The User who created the Network Map.
        name (str): The name of the Network Map.
        description (str): The description of the Network Map.
        is_public (bool): Flag for whether the Network Map is public to others.
            Defaults to False.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Node(models.Model):
    """
    Model for storing nodes.
    
    Args:
        name (str): The name of the Node.
        parent (:obj: network_map.Node): The parent Node
    """
    network_map = models.ForeignKey(
        NetworkMap,
        related_name='nodes',
        on_delete=models.CASCADE
    )
    id = models.CharField(max_length=100, primary_key=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    selectable = models.BooleanField(default=True)
    locked = models.BooleanField(default=False)
    grabbable = models.BooleanField(default=True)
    pannable = models.BooleanField(default=False)
    classes = models.CharField(max_length=255)
    style = models.JSONField(null=True, blank=True)
    scratch = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.id
    

class Edge(models.Model):
    """
    
    """

