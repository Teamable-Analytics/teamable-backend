class PASSWORD:
    REQUIRED = "Password is required."
    INVALID = (
        "Unable to log in with provided credentials. "
        "If you have forgotten your password try to reset your password."
    )

    ERROR_MESSAGES = {
        "required": REQUIRED,
        "null": REQUIRED,
        "blank": REQUIRED,
        "invalid": INVALID,
    }
