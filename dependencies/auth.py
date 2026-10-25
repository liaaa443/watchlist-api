from fastapi import Header, HTTPException, status

API_KEY = "watchlist-secret-key"


def verify_api_key(
    x_api_key: str | None = Header(default=None),
) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key tidak valid atau tidak diberikan",
        )
