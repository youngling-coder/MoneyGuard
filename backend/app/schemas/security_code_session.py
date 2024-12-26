from pydantic import EmailStr, BaseModel


class SecurityCodeSession(BaseModel):
    email: EmailStr


class RequestSecurityCodeSession(SecurityCodeSession):
    pass


class VerifySecurityCodeSession(BaseModel):
    security_code_session_token: str
    security_code: str


class CreateSecurityCodeSession(VerifySecurityCodeSession):
    pass
