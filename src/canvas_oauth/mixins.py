from django.contrib.auth.mixins import AccessMixin

from canvas_oauth.oauth import get_oauth_token


class TokenRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        access_token = get_oauth_token(request)
        return super().dispatch(request, *args, **kwargs)
