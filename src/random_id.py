import random
import string

# TODO: Gather requirements for acceptable id values. Should IDs be case insensitive?\
# https://stackoverflow.com/questions/2511222/efficiently-generate-a-16-character-alphanumeric-string
def generate_random_id(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_url_id() -> str:
    return generate_random_id(7)

def generate_auth_token() -> str:
    return generate_random_id(16)
