from pydantic import EmailStr, BaseModel


class SecurityCodeSession(BaseModel):
    email: EmailStr


class RequestSecurityCodeSession(SecurityCodeSession):
    pass


class CreateSecurityCodeSession(BaseModel):
    security_code_session_token: str | None = None
    security_code: str | None = None
