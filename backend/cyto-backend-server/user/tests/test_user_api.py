"""Unit tests for the User API."""
from datetime import date
from ..models import PersonalAccessToken
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class PublicUserAPITests(TestCase):
    """Test unauthenticated user endpoints."""

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
            'name': 'Test Name',
        }
        res = self.client.post(self.create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload.get('email'))
        self.assertTrue(user.check_password(payload.get('password')))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test emails are unique."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        self.create_user(**payload)
        res = self.client.post(self.create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test password length."""
        payload = {'email': 'test@example.com', 'password': 'pw', 'name': 'Test Name'}
        res = self.client.post(self.create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email=payload.get('email')).exists()
        )

    def test_authenticate_user(self):
        """Test authenticating a user."""
        user_details = {
            'email': 'test@example.com',
            'name': 'test_user',
            'password': 'testpass123',
        }
        self.create_user(**user_details)
        user_details.pop('name')
        res = self.client.post(self.token_url, user_details)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_verify_PAT(self):
        """Test verifying valid PAT is successful."""
        user_details = {
            'email': 'test@example.com',
            'name': 'test_user',
            'password': 'testpass123',
        }
        user = self.create_user(**user_details)

        token_string, _ = PersonalAccessToken.objects.create(
            user=user,
            name='Test_Token'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'PAT {token_string}')
        pat_verify_url = reverse('user:pat_verify')
        res = self.client.get(pat_verify_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_verify_fake_PAT(self):
        """Test verifying a fake token fails."""
        user_details = {
            'email': 'test@example.com',
            'name': 'test_user',
            'password': 'testpass123',
        }
        user = self.create_user(**user_details)
    
        token_string, _ = PersonalAccessToken.objects.create(
            user=user,
            name='Test_Token'
        )
        pat_verify_url = reverse('user:pat_verify')
        self.client.credentials(HTTP_AUTHORIZATION='PAT FAKE_TOKEN')
        res = self.client.get(pat_verify_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_expired_PAT(self):
        """Test verifying expired token fails."""
        user_details = {
            'email': 'test@example.com',
            'name': 'test_user',
            'password': 'testpass123',
        }
        user = self.create_user(**user_details)

        token_string, PAT = PersonalAccessToken.objects.create(
            user=user,
            name='Test_Token',
            expires=date(2000, 1, 1)
        )
        pat_verify_url = reverse('user:pat_verify')
        self.client.credentials(HTTP_AUTHORIZATION=f'PAT {token_string}')
        res = self.client.get(pat_verify_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        PAT.refresh_from_db()
        self.assertTrue(PAT.is_expired)

    def test_get_user_unauthenticated(self):
        """Test getting a user fails when unauthenticated."""
        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test authenticated user endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.me_url = reverse('user:me')
        user_details = {
            'email': 'test@example.com',
            'name': 'test_user',
            'password': 'testpass123',
        }
        self.user = self.create_user(**user_details)
        self.client.force_authenticate(user=self.user)

    def create_user(self, **params):
        """Create a new user."""
        return get_user_model().objects.create_user(**params)

    def test_retrieve_user(self):
        """Test retrieving user."""
        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name, 'email': self.user.email})

    def test_update_user(self):
        """Test updating a user."""
        payload = {'name': 'Updated Name', 'password': 'newpass123'}
        res = self.client.patch(self.me_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload.get('name'))
        self.assertTrue(self.user.check_password(payload.get('password')))
