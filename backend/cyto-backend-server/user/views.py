"""
The views for the User API.
"""
from user.models import PersonalAccessToken
from user import serializers
from user.pat_auth import PersonalAccessTokenAuthentication
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.translation import gettext_lazy as _


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    authentication_classes = []
    serializer_class = serializers.UserSerializer



class PATViewSet(viewsets.ModelViewSet):
    """"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.PATSerializer
    queryset = PersonalAccessToken.objects.all()

    def get_serializer_class(self):
        """"""
        if self.action == 'create':
            return serializers.PATCreateSerializer

        else:
            return self.serializer_class

    def get_queryset(self):
        """"""
        return (
            self.queryset
            .filter(user=self.request.user)
            .order_by('-id')
            .distinct()
        )

    def create(self, request, *args, **kwargs):
        """"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        token, PAT = serializer.save(user=request.user)

        response_data = {
            'id': PAT.id,
            'name': PAT.name,
            'created': PAT.created,
            'token': token,
            'revoked': PAT.revoked,
            'expires': PAT.expires,
            'is_expired': PAT.is_expired
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


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
