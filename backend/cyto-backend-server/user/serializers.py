"""
Serializers for the User API endpoints.
"""
from datetime import date
from .models import PersonalAccessToken 
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating a User."""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        """Create a new User."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing User."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate a user"""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = _("Unable to authenticate with the provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class PATCreateSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = PersonalAccessToken
        fields = [
            'name', 'expires',
        ]

    def create(self, validated_data):
        """Create a New Personal Access Token."""
        token, PAT = PersonalAccessToken.objects.create(
            **validated_data,
        )
        return token, PAT


class PATSerializer(PATCreateSerializer):
    """"""
    class Meta(PATCreateSerializer.Meta):
        fields = PATCreateSerializer.Meta.fields + [
            'id', 'created', 'revoked', 'is_expired'
        ]
    
    def update(self, instance, validated_data):
        """"""
        does_expire = date(validated_data.pop('expires', None))
        if does_expire:
            expires_date = date(does_expire)
            setattr(instance, 'expires', expires_date)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance