import secrets


def generate_security_code(length: int) -> str:
    return f"{secrets.randbelow(9 ** length+1):0{length}}"