from typing import Dict

from django_stubs_ext import StrOrPromise


class PASSWORD:
    REQUIRED = "Password is required."
    INVALID = (
        "Unable to log in with provided credentials. "
        "If you have forgotten your password try to reset your password."
    )

    ERROR_MESSAGES: Dict[str, StrOrPromise] = {
        "required": REQUIRED,
        "null": REQUIRED,
        "blank": REQUIRED,
        "invalid": INVALID,
    }
