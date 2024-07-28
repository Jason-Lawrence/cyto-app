from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from rest_framework import status
from rest_framework.test import APIClient


class PublicUserAPITests(TestCase):
    """Test User Authentication"""
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('user:create')
        self.token_url = reverse('user:token_create')
        self.me_url = reverse('user:me')

    def create_user(self, **params):
        """Create a new user."""
        return get_user_model().objects.create_user(**params)

    def test_create_user_success(self):
        """Test creating a new user."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        res = self.client.post(self.create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload.get('email'))
        self.assertTrue(
            user.check_password(payload.get('password'))
        )
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test emails are unique."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }
        self.create_user(**payload)
        res = self.client.post(self.create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test password length."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name'
        }
        res = self.client.post(self.create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(
                email=payload.get('email')
            ).exists()
        )

    def test_authenticate_user(self):
        """Test authenticating a user."""
        user_details = {
            'email': 'test@example.com',
            'name': 'test_user',
            'password': 'testpass123'
        }
        user = self.create_user(**user_details)
        user_details.pop('name')
        res = self.client.post(self.token_url, user_details)
        self.assertEqual(res.status_code, status.HTTP_200_OK)