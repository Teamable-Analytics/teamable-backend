from functools import wraps
from canvas_oauth.oauth import get_oauth_token


def token_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        access_token = get_oauth_token(request)
        return func(request, *args, **kwargs)

    return inner
