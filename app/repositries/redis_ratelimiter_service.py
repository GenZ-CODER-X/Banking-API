import json 
from app.core.redis_client import redis_client
import redis

class RedisRateLimiter():
    def __init__(self):
        self.WINDOW_SIZE = 60
        self.KEY_TTL = self.WINDOW_SIZE * 2
    
    def get_rate_limit_data(self,key):
        response=redis_client.get(key)
        if response is None:
            return None
        return json.loads(response)

    def save_rate_limit_data(self,key,previous_count,current_count,window_start):
        data={
            "previous_count":previous_count,
            "current_count":current_count,
            "window_start":window_start
        }
        redis_client.set(
            key,
            json.dumps(data),
            ex=self.KEY_TTL
        )

    def delete_rate_limit_data(key):
        redis_client.delete(key)

    def execute_transaction(self, key, callback):
        while True:
            pipe = redis_client.pipeline()

            try:
                pipe.watch(key)

                value = pipe.get(key)
    
                if value is not None:
                    value = json.loads(value)

                allowed, new_value = callback(value)

                if not allowed:
                    return False

                pipe.multi()

                pipe.set(
                    key,
                    json.dumps(new_value),
                    ex=self.KEY_TTL
                )

                pipe.execute()

                return True

            except redis.WatchError:
                continue

            finally:
                pipe.reset()