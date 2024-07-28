"""Test Node API endpoints."""
from rest_framework import status
from .common import BaseAPITests
from .. import models, serializers


class PublicNodeAPITests(BaseAPITests):
    """Test unauthenticated requests fail."""
    def setUp(self):
        super().setUp()
        self.endpoint = 'node'

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
        self.endpoint = 'node'
        self.user = self.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)
        self.network_map = self.create_network_map(user=self.user)

    def test_retrieve_nodes(self):
        """Test retrieving the nodes from a network map."""
        self.create_node(self.network_map)
        res = self.client.get(self.nested_list_url(self.network_map.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        nodes = models.Node.objects.all().order_by('-id')
        serializer = serializers.NodeSerializer(nodes, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_get_node_detail(self):
        """Test getting a nodes details."""
        node = self.create_node(self.network_map)
        res = self.client.get(
            self.nested_detail_url(self.network_map.id, node.id)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = serializers.NodeDetailSerializer(node)
        self.assertEqual(res.data, serializer.data)

    def test_create_node(self):
        """Test creating a node."""
        payload = {
            'label': 'Node 1',
            'x': 1, 
            'y': 1,
            'classes': 'triangle stuff',
        }
        res = self.client.post(
            self.nested_list_url(self.network_map.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        node = models.Node.objects.get(id=res.data.get('id'))
        for k, v in payload.items():
            self.assertEqual(getattr(node, k), v)
        self.assertEqual(node.parent, None)

    def test_partial_update(self):
        """Test partial update of node."""
        node = self.create_node(self.network_map)
        payload = {
            'label': 'New node label'
        }
        res = self.client.patch(
            self.nested_detail_url(self.network_map.id, node.id),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        node.refresh_from_db()
        self.assertEqual(node.label, payload.get('label'))

    def test_full_update(self):
        """Test fully updating a node."""
        node = self.create_node(self.network_map)
        payload = {
            'label': 'Node 2',
            'x': 2,
            'y': 2,
            'classes': 'square things',
            'selectable': False,
            'locked': True,
            'pannable': True,
            'style': {
                'width': '50px'
            },
            'scratch': {
                'key1': 'val1'
            }
        }
        res = self.client.put(
            self.nested_detail_url(self.network_map.id, node.id),
            payload,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        node.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(node, k), v)

    def test_delete_node(self):
        """Test deleting a node."""
        node = self.create_node(self.network_map)
        res = self.client.delete(
            self.nested_detail_url(self.network_map.id, node.id)
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            models.Node.objects
            .filter(id=node.id)
            .exists()
        )
