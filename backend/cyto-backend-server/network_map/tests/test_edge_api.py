"""Test Edge API endpoints."""
from rest_framework import status
from .common import BaseAPITests
from .. import models, serializers


class PublicNodeAPITests(BaseAPITests):
    """Test unauthenticated requests fail."""
    def setUp(self):
        super().setUp()
        self.endpoint = 'edge'

    def test_auth_required(self):
        """Test user must be authenticated."""
        user = self.create_user()
        network_map = self.create_network_map(user=user)
        res = self.client.get(self.nested_list_url(network_map.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNodeAPITests(BaseAPITests):
    """Test Authenticated endpoints."""
    def setUp(self):
        super().setUp()
        self.endpoint = 'edge'
        self.user = self.create_user()
        self.client.force_authenticate(self.user)
        self.network_map = self.create_network_map(user=self.user)
        self.node1 = self.create_node(self.network_map)
        self.node2 = self.create_node(self.network_map, **{'label': 'Node 2'})

    def test_retrieve_edges(self):
        """Test retrieving the edges from a network map."""
        self.create_edge(self.network_map, self.node1, self.node2)
        res = self.client.get(self.nested_list_url(self.network_map.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        edges = models.Edge.objects.all().order_by('-id')
        serializer = serializers.EdgeSerializer(edges, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_get_edge_details(self):
        """Test get edge details."""
        edge = self.create_edge(self.network_map, self.node1, self.node2)
        res = self.client.get(
            self.nested_detail_url(self.network_map.id, edge.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_edge(self):
        """Test create an edge."""
        payload = {
            'label': 'edge_1',
            'source': self.node1.id,
            'target': self.node2.id,
        }
        res = self.client.post(
            self.nested_list_url(self.network_map.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        edge = models.Edge.objects.get(id=res.data.get('id'))
        self.assertEqual(edge.label, payload.get('label'))
        self.assertEqual(edge.source, self.node1)
        self.assertEqual(edge.target, self.node2)

    def test_partial_update(self):
        """Test partially updating an edge."""
        edge = self.create_edge(self.network_map, self.node1, self.node2)
        payload = {
            'label': 'New Edge Label'
        }
        res = self.client.patch(
            self.nested_detail_url(self.network_map.id, edge.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        edge.refresh_from_db()
        self.assertEqual(edge.label, payload.get('label'))

    def test_full_update(self):
        """Test fully updating an edge."""
        edge = self.create_edge(self.network_map, self.node1, self.node2)
        payload = {
            'label': 'New Edge Label',
            'source': self.node2.id,
            'target': self.node1.id
        }
        res = self.client.put(
            self.nested_detail_url(self.network_map.id, edge.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        edge.refresh_from_db()
        self.assertEqual(edge.label, payload.get('label'))
        self.assertEqual(edge.source, self.node2)
        self.assertEqual(edge.target, self.node1)

    def test_delete_edge(self):
        """Test deleting an edge"""
        edge = self.create_edge(self.network_map, self.node1, self.node2)
        res = self.client.delete(
            self.nested_detail_url(self.network_map.id, edge.id)
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            models.Edge.objects
            .filter(id=edge.id)
            .exists()
        )
