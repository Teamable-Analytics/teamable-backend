from typing import Dict
from django_stubs_ext import StrOrPromise


class EMAIL:
    UNIQUE = (
        "A user with this email already exists. "
        "If you have forgotten your password try to reset your password."
    )
    REQUIRED = "Email is required."
    INVALID = "Email is invalid."

    ERROR_MESSAGES: Dict[str, StrOrPromise] = {
        "required": REQUIRED,
        "null": REQUIRED,
        "blank": REQUIRED,
        "invalid": INVALID,
    }
