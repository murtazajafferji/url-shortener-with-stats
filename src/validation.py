import re
from typing import Tuple, Optional

import validators

# Source: https://github.com/robertlit/redirector/blob/master/app/validation.py
def validate_request_body(data) -> Tuple[bool, Optional[str]]:
    if not isinstance(data, dict):
        return False, "Request body must be JSON object"

    fields = [
        ("url", str, validate_url, True),
        ("id", str, validate_url_id, False),
        ("authToken", str, validate_auth_token, False),
    ]

    for field_name, field_type, field_validate, required in fields:
        if field_name not in data:
            if required:
                return False, f"Missing {field_name}"

            continue

        if not isinstance(data[field_name], field_type):
            return False, f"Invalid type for {field_name}: {field_type.__name__} expected"

        is_valid_field, field_err_msg = field_validate(data[field_name])
        if not is_valid_field:
            return False, field_err_msg

    return True, None

# TODO: Get requirements for url id validation. Examples had all lowercase, but this is not currently enforeced.
def validate_url_id(url_id: str) -> Tuple[bool, Optional[str]]:
    pattern = r"^[A-Za-z0-9]+$" # validates that IDs are non-empty and only contain alphanumeric characters
    if not re.match(pattern, url_id):
        return False, "urlId must consist of letters and digits"

    return True, None


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    if not validators.url(url):
        return False, "The URL is not valid"

    return True, None


def validate_auth_token(url: str) -> Tuple[bool, Optional[str]]:
    if not validators.url(url):
        return False, "The URL is not valid"

    return True, None