"""
The views for the User API.
"""

from user import serializers
from user.pat_auth import PersonalAccessTokenAuthentication
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.translation import gettext_lazy as _


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    authentication_classes = []
    serializer_class = serializers.UserSerializer


class PATVerifyView(APIView):
    """Verify a Personal Access Token."""
    authentication_classes = [PersonalAccessTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Verify PAT is Valid."""
        msg = _(f'User: {request.user.name} is authenticated!')
        return Response({'msg': msg}, status=status.HTTP_200_OK)

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage Authenticated user."""
    serializer_class = serializers.UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
