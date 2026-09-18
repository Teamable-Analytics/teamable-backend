class CanvasOAuthError(Exception):
    pass


class MissingTokenError(CanvasOAuthError):
    pass


class InvalidOAuthStateError(CanvasOAuthError):
    pass


class InvalidOAuthReturnError(CanvasOAuthError):
    pass


class InvalidGrantError(InvalidOAuthReturnError):
    """Canvas no longer recognizes the grant (e.g. the refresh token was revoked)"""

    pass
