from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone


class CanvasOAuth2Token(models.Model):
    """
    A CanvasOAuth2Token instance represents the access token
    response from Canvas when the user requests an authorization
    grant as in :rfc:`6749`.  Canvas tokens are short-lived, and
    so they issue refresh tokens as part of the grant response.
    The refresh tokens are used to retrieve new access tokens once
    they expire.
    Fields:
    * :attr:`user` The Django user representing resources' owner
    * :attr:`access_token` Access token
    * :attr:`refresh_token` Refresh token
    * :attr:`expires` Date and time of token expiration, in DateTime format
    * :attr:`created_on` When the initial access token was granted,
        in DateTime format
    * :attr:`updated_on` When the token was refreshed (or first created), in
        DateTime format
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="canvas_oauth2_token",
    )
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def expires_within(self, delta):
        """
        Check token expiration with timezone awareness within
        the given amount of time, expressed as a timedelta.

        :param delta: The timedelta to check expiration against
        """
        if not self.expires:
            return False

        return self.expires - timezone.now() <= delta
