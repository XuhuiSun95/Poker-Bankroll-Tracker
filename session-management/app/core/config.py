from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True)

    OIDC_AUTHORIZATION_URL: str
    OIDC_TOKEN_URL: str
    OIDC_JWKS_URL: str
    OIDC_CLIENT_ID: str = "poker-bankroll-tracker"
    OIDC_PERMITTED_AUDIENCES: list[str] = ["account"]

    OIDC_APPLICATION_SCOPES_ENABLED: bool = False


settings = Settings()
