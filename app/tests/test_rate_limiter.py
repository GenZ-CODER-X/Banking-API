from types import SimpleNamespace

from app.services.rate_limiter_service import is_request_allowed


key_string_data = SimpleNamespace(
    key="user_id",
    value="123"
)

endpoint = "/test-rate-limit"

for i in range(21):
    result = is_request_allowed(
        endpoint,
        key_string_data
    )

    print(f"Request {i + 1}: {result}")