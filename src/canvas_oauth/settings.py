# -*- coding: utf-8 -*-
"""
canvas_oauth specific settings
"""
from __future__ import unicode_literals
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def get_required_setting(oauth_setting):
    """
    Check for and return required OAuth setting here so we can
    raise an error if not found.
    """
    if not hasattr(settings, oauth_setting):
        raise ImproperlyConfigured(
            "Missing %s setting that is required to use the Django Canvas OAuth library"
            % oauth_setting
        )
    return getattr(settings, oauth_setting)


# Get required settings from project conf
CANVAS_OAUTH_CLIENT_ID = get_required_setting("CANVAS_OAUTH_CLIENT_ID")
CANVAS_OAUTH_CLIENT_SECRET = get_required_setting("CANVAS_OAUTH_CLIENT_SECRET")

# fixme: This value is hardcoded through environment variables. If multiple
#  organizations with multiple Canvas API urls are added in the future,
#  this will need to be defined per-organization
CANVAS_OAUTH_CANVAS_DOMAIN = get_required_setting("CANVAS_OAUTH_CANVAS_DOMAIN")

# Optional settings
# -----------------

# A buffer for refreshing a token when retrieving via `get_token`, expressed
# as a timedelta.  Default to having no expiration buffer.
CANVAS_OAUTH_TOKEN_EXPIRATION_BUFFER = getattr(
    settings,
    "CANVAS_OAUTH_TOKEN_EXPIRATION_BUFFER",
    timedelta(),
)

CANVAS_OAUTH_ERROR_TEMPLATE = getattr(
    settings, "CANVAS_OAUTH_ERROR_TEMPLATE", "oauth_error.html"
)
