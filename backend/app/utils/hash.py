from passlib.context import CryptContext


crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash(plain: str) -> str:
    return crypt_context.hash(plain)


def verify_hash(plain: str, hash: str) -> bool:
    return crypt_context.verify(plain, hash)
