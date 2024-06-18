from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from django.conf import settings


from rest_framework import generics, permissions, status, serializers, authentication
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from drf_spectacular.utils import extend_schema, inline_serializer

from user import serializers


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    authentication_classes = []
    serializer_class = serializers.UserSerializer 
    

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage Authenticated user."""
    serializer_class = serializers.UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
    