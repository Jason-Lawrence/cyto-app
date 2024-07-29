"""Shared functionality for Test Cases."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from .. import models


class BaseAPITests(TestCase):
    """Base class for Network Map app unit tests."""
    def setUp(self):
        self.client = APIClient()
        self.endpoint = None  # edges or nodes

    def network_map_detail_url(self, network_map_id):
        """Reverse lookup the url path for network map detail."""
        return reverse('network_map:networkmap-detail', args=[network_map_id])

    def network_map_list_url(self):
        """Reverse lookup the url path for network map list."""
        return reverse('network_map:networkmap-list')

    def nested_detail_url(self, network_map_id, nested_id):
        """Reverse lookup the url path for nested item's details"""
        return reverse(
            f'network_map:{self.endpoint}-detail',
            args=[network_map_id, nested_id]
        )

    def nested_list_url(self, network_map_id):
        """Reverse lookup the url path for nested item's list"""
        return reverse(
            f'network_map:{self.endpoint}-list',
            args=[network_map_id]
        )

    def create_user(self, **params):
        """Create a test user."""
        defaults = {
            'email': 'test@example.com', 
            'password': 'testpass123'
        }
        defaults.update(params)
        return get_user_model().objects.create_user(**defaults)

    def create_network_map(self, user, **params):
        """Create a test network map."""
        defaults = {
            'name': 'Test Map',
            'description': 'Test Description',
            'layout': {'name': 'preset'},
            'is_public': False,
        }
        defaults.update(params)
        return models.NetworkMap.objects.create(user=user, **defaults)

    def create_node(self, network_map, parent=None, **params):
        """Create a test node."""
        defaults = {
            'label': 'Node 1',
            'x': 1,
            'y': 1,
            'classes': 'triangle stuff',
        }
        defaults.update(params)
        return models.Node.objects.create(
            network_map=network_map, parent=parent, **defaults
        )

    def create_edge(self, network_map, source, target, **params):
        """Create a test edge."""
        defaults = {
            'label': 'edge label',
        }
        defaults.update(params)
        return models.Edge.objects.create(
            network_map=network_map, source=source, target=target, **defaults
        )
