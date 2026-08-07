from repositries.redis_ratelimiter_service import RedisRateLimiter
import time

def generate_key(endpoint,key_string_data):
    key=f"rate_limit:user:{key_string_data.key}:{key_string_data.value}:{endpoint}"





def is_request_allowed():






def create_new_window(key):
    now=int(time.time())
    window_start=now-(now%60)
    RedisRateLimiter.save_rate_limit_data(key,0,1,window_start)

def rotate_window():






def calculate_effective_count():






def get_data_from_redis(key):
    rate_limiter_response=RedisRateLimiter.get_rate_limit_data(key)
    if rate_limiter_response is None:
        create_new_window(key)
    else:
        rotate_window(key,rate_limiter_response)
