from fastapi import HTTPException,status
from app.services.rate_limiter_service import is_request_allowed
def rate_limit(user_id: str, endpoint: str):
    key_string_data = {
        "key": "user_id",
        "value": user_id
    }
    allowed = is_request_allowed(
        endpoint,
        key_string_data
    )
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )