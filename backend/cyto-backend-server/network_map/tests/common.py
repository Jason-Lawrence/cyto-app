"""Shared functionality for Test Cases."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .. import models


class BaseAPITests(TestCase):
    """"""
    def setUp(self):
        self.client = APIClient()
        self.endpoint = None # edges or nodes

    def network_map_detail_url(self, network_map_id):
        """"""
        return reverse(
            'network_map:networkmap-detail',
            args=[network_map_id]
        )

    def network_map_list_url(self):
        """"""
        return reverse(
            'network_map:networkmap-list'
        )

    def nested_detail_url(self, network_map_id, nested_id):
        """"""
        return reverse(
            f'network_map:{self.endpoint}-detail',
            args=[network_map_id, nested_id]
        )

    def nested_list_url(self, network_map_id):
        """"""
        return reverse(
            f'network_map:{self.endpoint}-list',
            args=[network_map_id]
        )

    def create_user(self, **params):
        """"""
        defaults = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        defaults.update(params)
        return get_user_model().objects.create_user(**defaults)

    def create_network_map(self, user, **params):
        """"""
        defaults = {
            'name': 'Test Map',
            'description': 'Test Description',
            'layout': {
                'name': 'preset'
            },
            'is_public': False,
        }
        defaults.update(params)
        return models.NetworkMap.objects.create(user=user, **defaults)
