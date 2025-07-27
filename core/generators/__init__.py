import secrets

def default_subid_generator(nbytes: int = 48) -> str:
    return secrets.token_urlsafe(nbytes)
