"""Test for Network Map API"""
from .common import BaseAPITests

from rest_framework import status
from rest_framework.test import APIClient
from django.db.models import Q

from .. import models, serializers


class PublicNetworkMapAPITests(BaseAPITests):
    """Test unauthenticated requests."""
    def test_auth_required(self):
        """Test user must be authenticated."""
        res = self.client.get(self.network_map_list_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNetworkMapAPITests(BaseAPITests):
    """Test authenticated endpoints"""
    def setUp(self):
        super().setUp()
        self.user = self.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_network_maps(self):
        """"""
        self.create_network_map(user=self.user)
        res = self.client.get(self.network_map_list_url())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        network_maps = models.NetworkMap.objects.all().order_by('-id')
        serializer = serializers.NetworkMapSerializer(network_maps, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_network_maps_limited_user_or_public(self):
        """
        Test retrieving network maps only returns network maps that 
        are public or belonging to the user.
        """
        other_user = self.create_user(
            email='other@example.com',
            password='otherpass123'
        )
        self.create_network_map(user=self.user)
        self.create_network_map(user=other_user)
        self.create_network_map(
            user=other_user,
            **{'is_public': True}
        )
        res = self.client.get(self.network_map_list_url())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        network_maps = (
            models.NetworkMap.objects
            .all()
            .filter(
                Q(user=self.user) | Q(is_public=True)
            )
            .order_by('-id')
        )
        serializer = serializers.NetworkMapSerializer(network_maps, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_get_network_map_detail(self):
        """Test getting a network maps details."""
        network_map = self.create_network_map(user=self.user)
        res = self.client.get(
            self.network_map_detail_url(network_map.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = serializers.NetworkMapDetailSerializer(network_map)
        self.assertEqual(res.data, serializer.data)

    def test_create_network_map(self):
        """Test creating a network map."""
        payload = {
            'name': 'Test map',
            'description': 'Test description',
            'layout': {
                'name': 'circle'
            },
            'is_public': True
        }
        res = self.client.post(
            self.network_map_list_url(), payload, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        network_map = models.NetworkMap.objects.get(id=res.data.get('id'))
        for k, v in payload.items():
            self.assertEqual(getattr(network_map, k), v)
        self.assertEqual(network_map.user, self.user)

    def test_partial_update(self):
        """Test partial update of a network map."""
        network_map = self.create_network_map(user=self.user)
        payload = {
            'name': 'New name'
        }
        res = self.client.patch(
            self.network_map_detail_url(network_map.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        network_map.refresh_from_db()
        self.assertEqual(network_map.name, payload.get('name'))

    def test_full_update(self):
        """Test fully updating a network map."""
        network_map = self.create_network_map(user=self.user)
        payload = {
            'name': 'New name',
            'description': 'new description',
            'layout': {
                'name': 'circle'
            },
            'is_public': True
        }
        res = self.client.put(
            self.network_map_detail_url(network_map.id),
            payload,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        network_map.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(network_map, k), v)
        self.assertEqual(network_map.user, self.user)

    def test_delete_network_map(self):
        """Test deleting a network map."""
        network_map = self.create_network_map(user=self.user)
        res = self.client.delete(self.network_map_detail_url(network_map.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            models.NetworkMap.objects
            .filter(id=network_map.id)
            .exists()
        )
