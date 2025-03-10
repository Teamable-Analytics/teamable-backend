from canvas_oauth.exceptions import MissingTokenError, CanvasOAuthError
from canvas_oauth.oauth import handle_missing_token, render_oauth_error


class OAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    """On catching a MissingTokenError - as is raised by the get_token function
    if there is no saved token for the user - this begins the oauth dance with
    canvas to get a new token.  For other CanvasOAuthErrors, an error page with
    the exception text is rendered."""

    def process_exception(self, request, exception):
        if isinstance(exception, MissingTokenError):
            return handle_missing_token(request)
        elif isinstance(exception, CanvasOAuthError):
            return render_oauth_error(str(exception))
        return
