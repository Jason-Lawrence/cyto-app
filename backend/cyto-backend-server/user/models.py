"""
Models for the User app.
"""
from datetime import date
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """Custom Manager for User Objects"""

    def create_user(self, email, password=None, **extra_fields):
        """Create a User Object"""
        if not email:
            raise ValueError("Email is required.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create a Super User"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self.db)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class PersonalAccessTokenManager(models.Manager):
    """Personal Access Token Manager."""
    def generate_token(self):
        """Generate a 32 byte token."""
        return get_random_string(32)

    def hash_token(self, token):
        """Hash Token to store in Database."""
        return make_password(token)

    def create(self, user, name, **extra_fields):
        """
        Create a Personal Access Token.
        
        Args:
            user (:class: User): The user the token belongs too.
            name (str): The name for the token.
            extra_fields (kwargs): Other fields for a PAT.
        
        Returns:
            token_string (str): The string to present to the User.
            PAT (:class: PersonalAccessToken): The PAT object.
        """
        if not name:
            raise ValueError('Name is required.')

        token_string = self.generate_token()
        token_hash = self.hash_token(token_string)
        PAT = self.model(
            user=user,
            name=name,
            token=token_hash,
            **extra_fields
        )
        PAT.save(using=self.db)
        return token_string, PAT

    def check_expiration(self, token):
        """
        Check token's expiration.
        
        Args:
            token (str): The token to check.
            
        Return:
            is_expired (bool): True if expired else False.
        """
        if token.expires is None:
            return False
    
        elif token.expires > date.today():
            return False

        else:
            token.is_expired = True
            token.save()
            return True


class PersonalAccessToken(models.Model):
    """
    Personal Access Token to use for Authentication. 
    Primarily to be used with automation scripts.
    
    Args:
        user (:class: User): The user the token belongs too.
        name (str): The name for the token.
        created (:class: date): When the PAT was created.
        expires (:class: date): When the PAT expires. 
            If None the token never expires.
        revoked (bool): Whether the token has been revoked.
        is_expired (bool): Whether the PAT has expired.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    token = models.CharField(max_length=88)
    name = models.CharField(max_length=50)
    created = models.DateField(auto_now=False, auto_now_add=True)
    expires = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )
    revoked = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    
    objects = PersonalAccessTokenManager()
    
    def __str__(self):
        return self.name
