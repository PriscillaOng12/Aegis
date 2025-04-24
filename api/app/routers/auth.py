"""Authentication router for token exchange."""

from fastapi import APIRouter
from ..schemas import TokenExchangeRequest, TokenExchangeResponse

router = APIRouter()


@router.post("/auth/exchange", response_model=TokenExchangeResponse)
async def exchange_token(payload: TokenExchangeRequest) -> TokenExchangeResponse:
    """Exchange an Auth0 code for an access token.

    In local development, this returns a static token. In production, this
    would call Auth0’s token endpoint with the client secret and code.
    """
    # Stub: return static dev token and 1 hour expiry
    return TokenExchangeResponse(
        access_token="dev-token",
        expires_in=3600,
        refresh_token=None,
    )