from app.repositries.redis_ratelimiter_service import RedisRateLimiter
import time

redis=RedisRateLimiter()

def generate_key(endpoint,key_string_data):
    key=f"rate_limit:{key_string_data.key}:{key_string_data.value}:{endpoint}"
    return key

def is_request_allowed(endpoint, key_string_data):
    limit = 20
    key = generate_key(endpoint, key_string_data)
    def rate_limit_callback_fxn(rate_limiter_response):
        if rate_limiter_response is None:
            new_data = create_new_window()
            return True, new_data
        windows_passed = rotate_window(rate_limiter_response)
        now = int(time.time())
        window_start = now - (now % 60)
        if windows_passed == 1:
            new_data = {
                "previous_count": rate_limiter_response["current_count"],
                "current_count": 1,
                "window_start": window_start
            }
            return True, new_data
        if windows_passed > 1:
            new_data = {
                "previous_count": 0,
                "current_count": 1,
                "window_start": window_start
            }
            return True, new_data
        effective_count = calculate_effective_count(rate_limiter_response)
        if effective_count >= limit:
            return False, None
        new_data = {
            "previous_count": rate_limiter_response["previous_count"],
            "current_count": rate_limiter_response["current_count"] + 1,
            "window_start": rate_limiter_response["window_start"]
        }
        return True, new_data
    return redis.execute_transaction(
        key,
        rate_limit_callback_fxn
    )


#Withput using the redis transactions
# def is_request_allowed(endpoint,key_string_data):
#     limit=20
#     key=generate_key(endpoint,key_string_data)
#     def rate_limit_callback_fxn(rate_limiter_response):
#         # rate_limiter_response=get_data_from_redis(key)
#         if rate_limiter_response is None:
#             value=create_new_window()
#             redis.save_rate_limit_data(key,
#             value["previous_count"],
#             value["current_count"],
#             value["window_start"])
#             return True
#         else:
#             windows_passed=rotate_window(rate_limiter_response)
#             now = int(time.time())
#             window_start = now - (now % 60)
#             if windows_passed==1:
#                 redis.save_rate_limit_data(key,rate_limiter_response["current_count"],1,window_start)
#                 return True
#             if windows_passed>1:
#                 redis.save_rate_limit_data(key,0,1,window_start)
#                 return True
#             else:
#                 effective_count=calculate_effective_count(rate_limiter_response)
#                 if effective_count>=limit:
#                     return False
#                 redis.save_rate_limit_data(key,
#                 rate_limiter_response["previous_count"],
#                 rate_limiter_response["current_count"]+1,
#                 rate_limiter_response["window_start"])
#                 return True
#     redis.execute_transaction(
#     key,
#     rate_limit_callback_fxn
# )
def create_new_window():
    now=int(time.time())
    window_start=now-(now%60)
    return{
        "previous_count":0,
        "current_count":1,
        "window_start":window_start
    }

def rotate_window(rate_limiter_response):
#Here we count how many windows passed since the last upated  window_start 
#We will get the current time if window_end<present_time then rotate window taking current_count=1 nd previous_count=prev window current

#1.Check the time and compare the window_start if new window then directly allow the req or in the same window calculate the req_allowed or not
    current_time=int(time.time())
    elapsed=current_time-rate_limiter_response["window_start"]
    windows_passed=elapsed//60
    return windows_passed
        
def calculate_effective_count(rate_limiter_response):
#effective_count=curent_window+(%previous_window*prev_window_counter)
#if effective_count<limit allow the req return True else False
#elapsed = current_time - window_start and  weight = (WINDOW_SIZE - elapsed) / WINDOW_SIZE and 
#previous = 10   current = 14    elapsed = 30 sec    effective = 14 + (10 × 0.5)= 19
    elapsed=int(time.time())-rate_limiter_response["window_start"]
    weight=(60-elapsed)/60
    effective_count=rate_limiter_response["current_count"]+rate_limiter_response["previous_count"]*weight
    return effective_count


def get_data_from_redis(key):
    rate_limiter_response=redis.get_rate_limit_data(key)
    return rate_limiter_response
