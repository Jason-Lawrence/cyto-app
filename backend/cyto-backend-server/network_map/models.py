"""
Models for the Network Map app.
"""
from django.db import models
from django.conf import settings


class NetworkMap(models.Model):
    """
    Model for storing Network Maps.

    Args:
        user (:obj: user.User): The User who created the Network Map.
        name (str): The name of the Network Map.
        description (str): The description of the Network Map.
        layout (JSON): Store the Layout Properties.
        is_public (bool): Flag for whether the Network Map is public to others.
            Defaults to False.
        created_at (DateTime): When the Network Map was created.
        last_updated (Datetime): When the Network Map was last updated.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    layout = models.JSONField(default=dict)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.name


class Node(models.Model):
    """
    Model for storing nodes.

    Args:
        network_map(:obj: network_map.models.NetworkMap):
            The Network Map the node belongs too.
        id (str): The nodes Primary key.
        label (str): The nodes label.
        parent (:obj: network_map.models.Node): The parent Node
        x (float): The x position of the node.
        y (float): The y position of the node.
        selectable (bool): Whether the node's selection state is mutable.
        locked (bool): Whether the node's position is locked.
        grabbable (bool): Whether the node can be grabbed.
        pannable (bool): Whether dragging the causes panning.
        classes (str): Class names the node has.
        style (JSON): Style property overrides.
        scratch (JSON): Scratchpad data.
    """

    network_map = models.ForeignKey(
        NetworkMap, related_name='nodes', on_delete=models.CASCADE
    )
    nid = models.CharField(max_length=100)
    label = models.CharField(max_length=75)
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

    def save(self, *args, **kwargs):
        self.nid = self.label.replace(' ', '_').lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id


class Edge(models.Model):
    """
    Model for storing Edges.

    Args:
        network_map(:obj: network_map.models.NetworkMap):
            The Network Map the node belongs too.
        id (str): The edge's Primary Key.
        label (str): The edge's label.
        source (:obj: network_map.models.Node):
            The source node for the edge.
        target(:obj: network_map.models.Node):
            The target for the edge.
        pannable (bool): Whether dragging on the edge can cause panning.
    """

    network_map = models.ForeignKey(
        NetworkMap, related_name='edges', on_delete=models.CASCADE
    )
    eid = models.CharField(max_length=100)
    label = models.CharField(max_length=75)
    source = models.ForeignKey(
        Node, related_name='source_node', on_delete=models.CASCADE
    )
    target = models.ForeignKey(
        Node, related_name='target_node', on_delete=models.CASCADE
    )
    pannable = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.eid = f'edge_{self.source.nid} -> {self.target.nid}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id
