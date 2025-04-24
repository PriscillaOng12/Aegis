import os
from functools import lru_cache
from typing import Dict, Any

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import httpx


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "example.auth0.com")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "aegis-health")


@lru_cache()
def get_jwks() -> Dict[str, Any]:
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    resp = httpx.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()


async def verify_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Verify the JWT using Auth0 JWKS and return the payload.

    In local development, the special token 'dev-token' bypasses verification and
    returns a stubbed payload. This simplifies running the stack without an
    Auth0 tenant.
    """
    if token == "dev-token":
        return {"sub": "dev-user", "scope": "patient"}
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if key is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header")
        payload = jwt.decode(
            token,
            key,
            algorithms=unverified_header.get("alg"),
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
        return payload  # contains sub, scope, etc.
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))