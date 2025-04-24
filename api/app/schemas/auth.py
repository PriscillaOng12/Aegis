from pydantic import BaseModel, Field


class TokenExchangeRequest(BaseModel):
    auth_code: str = Field(..., description="Auth0 authorisation code")
    code_verifier: str = Field(..., description="PKCE code verifier")


class TokenExchangeResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str | None = None