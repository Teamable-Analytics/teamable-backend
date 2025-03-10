from canvas_oauth.oauth import oauth_callback, initiate_oauth_check
from django.urls import path

urlpatterns = [
    path("oauth-callback", oauth_callback, name="canvas-oauth-callback"),
    path("initiate", initiate_oauth_check, name="canvas-oauth-initiate"),
]
