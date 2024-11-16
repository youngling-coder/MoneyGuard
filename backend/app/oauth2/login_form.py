from typing import Annotated, Union
from fastapi import Form
from pydantic import EmailStr


class OAuth2EmailRequestForm:
    def __init__(
        self,
        *,
        grant_type: Annotated[
            Union[str, None],
            Form(pattern="password"),
        ] = None,
        email: Annotated[
            EmailStr,
            Form(),
        ],
        password: Annotated[
            str,
            Form(),
        ],
        scope: Annotated[
            str,
            Form(),
        ] = "",
        client_id: Annotated[
            Union[str, None],
            Form(),
        ] = None,
        client_secret: Annotated[
            Union[str, None],
            Form(),
        ] = None,
    ):
        self.grant_type = grant_type
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
