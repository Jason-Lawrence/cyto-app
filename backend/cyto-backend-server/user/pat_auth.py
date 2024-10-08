"""Authenticate a Personal Access Token."""
from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _

from .models import PersonalAccessToken


def get_authorization_header(request):
    """Get the authorization header."""
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        auth = auth.encode(HTTP_HEADER_ENCODING)

    return auth


class PersonalAccessTokenAuthentication(TokenAuthentication):
    """Handle the workflow of authenticating a PAT."""
    keyword = 'PAT'
    model = PersonalAccessToken

    def authenticate(self, request):
        """Override base class. check header and validate token."""
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        else:
            try:
                token = auth[1].decode()

            except UnicodeError:
                msg = _('Invalid token header. Token string contains illegal characters.')
                raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        """Validate token against all stored token."""
        auth_token = None
        stored_tokens = (PersonalAccessToken.objects
                            .filter(revoked=False, is_expired=False))
        for stored in stored_tokens:
            if check_password(token, stored.token):
                auth_token = stored
                break
        
        if not auth_token:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not PersonalAccessToken.objects.check_expiration(auth_token):
            return (auth_token.user, auth_token)
