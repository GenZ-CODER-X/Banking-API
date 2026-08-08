from repositries.redis_ratelimiter_service import RedisRateLimiter
import time
from fastapi import HTTPException,status

redis=RedisRateLimiter()

def generate_key(endpoint,key_string_data):
    key=f"rate_limit:user:{key_string_data.key}:{key_string_data.value}:{endpoint}"
    return key

def is_request_allowed(ans):
    if ans==False:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Request after 1 min ")
    else:
        #Here we will call the end point_serive or allow the req

def create_new_window(key):
    now=int(time.time())
    window_start=now-(now%60)
    redis.save_rate_limit_data(key,0,1,window_start)


def rotate_window(key,rate_limiter_response):
#Here we count how many windows passed since the last upated  window_start 
#We will get the current time if window_end<present_time then rotate window taking current_count=1 nd previous_count=prev window current

#1.Check the time and compare the window_start if new window then directly allow the req or in the same window calculate the req_allowed or not
    current_time=int(time.time())
    limit=20
    if current_time>key.window_start+60:
        RedisRateLimiter.save_rate_limit_data(key,rate_limiter_response.current_count,1,current_time-(current_time%60))
        is_request_allowed(True)

    else:
        count=calculate_effective_count(key,rate_limiter_response)
        if count>limit:
            is_request_allowed(False)
        else:
            is_request_allowed(True)
        
def calculate_effective_count(key,rate_limiter_response):
#effective_count=curent_window+(%previous_window*prev_window_counter)
#if effective_count<limit allow the req return True else False
    prev_window_req=
    effective_count=rate_limiter_response.current_count+()


def get_data_from_redis(key):
    rate_limiter_response=RedisRateLimiter.get_rate_limit_data(key)
    if rate_limiter_response is None:
        create_new_window(key)
    else:
        rotate_window(key,rate_limiter_response)
