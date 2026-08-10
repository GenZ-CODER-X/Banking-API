import redis
from app.core.redis_client import redis_client
key = "test:transaction"
redis_client.set(key, "10")
pipe = redis_client.pipeline()
try:
    pipe.watch(key)
    print("WATCH started")
    print("Value:", pipe.get(key))
    # We will simulate another request changing the key
    other_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
    other_client.set(key, "20")
    print("Another client changed the key")
    pipe.multi()
    pipe.set(key, "11")
    print("Executing transaction...")
    pipe.execute()
    print("Transaction succeeded")
except redis.WatchError:
    print("WatchError! Key was modified by another request.")
finally:
    pipe.reset()
    redis_client.delete(key)