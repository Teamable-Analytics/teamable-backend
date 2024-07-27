class PASSWORD:
    REQUIRED = "Password is required."
    INVALID = "Unable to log in with provided credentials."

    ERROR_MESSAGES = {
        "required": REQUIRED,
        "null": REQUIRED,
        "blank": REQUIRED,
        "invalid": INVALID,
    }
