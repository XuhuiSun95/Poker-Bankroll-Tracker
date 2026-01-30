from typing import Annotated, Any

import jwt
import strawberry
from fastapi import Depends, HTTPException, Security
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from strawberry.permission import BasePermission

from ..core.config import settings
from ..models.token import TokenPayload, TokenPayloadError

application_scopes = {
    f"{resource}:{action}": f"{action.title()} {resource}"
    for resource in ["session"]
    for action in ["read", "write"]
    if settings.OIDC_APPLICATION_SCOPES_ENABLED
}

oidc_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.OIDC_AUTHORIZATION_URL,
    tokenUrl=settings.OIDC_TOKEN_URL,
    scopes=application_scopes | {"openid": "OpenID"},
    auto_error=False,
)

TokenDependency = Annotated[str, Depends(oidc_scheme)]
jwks_client = jwt.PyJWKClient(settings.OIDC_JWKS_URL)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: TokenDependency,
) -> TokenPayload | TokenPayloadError:
    if not token:
        return TokenPayloadError(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
        token_payload = TokenPayload(**payload)
        for scope in security_scopes.scopes:
            if scope not in token_payload.scope:
                return TokenPayloadError(
                    status_code=403,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
    except (InvalidTokenError, ValidationError):
        return TokenPayloadError(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
    return token_payload


async def get_current_oidc_user(
    current_user: Annotated[
        TokenPayload | TokenPayloadError, Security(get_current_user, scopes=["openid"])
    ],
) -> TokenPayload:
    if isinstance(current_user, TokenPayloadError):
        raise HTTPException(
            status_code=current_user.status_code,
            detail=current_user.detail,
            headers=current_user.headers,
        )
    return current_user


async def get_current_oidc_user_no_exception(
    current_user: Annotated[
        TokenPayload | TokenPayloadError, Security(get_current_user, scopes=["openid"])
    ],
) -> TokenPayload | None:
    if isinstance(current_user, TokenPayloadError):
        return None
    return current_user


async def get_current_oidc_user_graphql_context(
    current_user: Annotated[
        TokenPayload | None, Depends(get_current_oidc_user_no_exception)
    ],
) -> dict[str, Any]:
    if current_user is None:
        return {}
    return {"current_user": current_user}


class IsAuthenticated(BasePermission):
    message = "Not authenticated"

    async def has_permission(
        self,
        source: Any,
        info: strawberry.Info,
        **kwargs: Any,
    ) -> bool:
        if "current_user" not in info.context:
            return False
        return True
