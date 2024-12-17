from passlib.context import CryptContext

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash(plain: str) -> str:
    return crypto_context.hash(plain)


def verify_hash(plain: str, hash: str) -> bool:
    return crypto_context.verify(plain, hash)
    