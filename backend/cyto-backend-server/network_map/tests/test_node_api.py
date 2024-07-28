""""""
from .common import BaseAPITests

from rest_framework import status


class PublicNodeAPITests(BaseAPITests):
    """"""
    def setUp(self):
        super().setUp()
        self.endpoint = 'node'

    def test_auth_required(self):
        """Test user must be authenticated."""
        user = self.create_user()
        network_map = self.create_network_map(user=user)
        res = self.client.get(self.nested_list_url(network_map.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
