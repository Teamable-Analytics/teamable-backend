from canvasapi import Canvas

from app.models import Organization
from canvas_oauth.oauth import get_oauth_token


def init_canvas(request, organization: Organization) -> Canvas:
    access_token = get_oauth_token(request)
    return Canvas(organization.lms_api_url, access_token)
