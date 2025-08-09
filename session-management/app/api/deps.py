from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from ..core.config import settings
from ..models.token import TokenPayload

application_scopes = {
    f"{resource}:{action}": f"{action.title()} {resource}"
    for resource in ["session"]
    for action in ["create", "read", "update", "delete"]
    if settings.OIDC_APPLICATION_SCOPES_ENABLED
}

oidc_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.OIDC_AUTHORIZATION_URL,
    tokenUrl=settings.OIDC_TOKEN_URL,
    scopes=application_scopes | {"openid": "OpenID"},
)

TokenDependency = Annotated[str, Depends(oidc_scheme)]
jwks_client = jwt.PyJWKClient(settings.OIDC_JWKS_URL)


def get_current_user(
    security_scopes: SecurityScopes,
    token: TokenDependency,
) -> TokenPayload:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scopes}"'
    else:
        authenticate_value = "Bearer"
    try:
        payload = jwt.decode(
            token,
            jwks_client.get_signing_key_from_jwt(token).key,
            algorithms=["RS256"],
            audience=settings.OIDC_PERMITTED_AUDIENCES,
        )
        print(payload)
        token_payload = TokenPayload(**payload)
        for scope in security_scopes.scopes:
            if scope not in token_payload.scope:
                raise HTTPException(
                    status_code=401,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
    except (InvalidTokenError, ValidationError) as err:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"
        ) from err
    return token_payload


def get_current_oidc_user(
    current_user: Annotated[
        TokenPayload, Security(get_current_user, scopes=["openid"])
    ],
) -> TokenPayload:
    return current_user
