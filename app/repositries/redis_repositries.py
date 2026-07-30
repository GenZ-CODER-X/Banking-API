import json 
from app.core.redis import redis_client

class RedisRepository():
    def get_response(self,idempotency_key:str):
        response=redis_client.get(idempotency_key)
        if response is None:
            return None
        return json.loads(response)

    def save_response(self,idempotency_key:str,response:dict):
        value=json.dumps(response)
        redis_client.set(idempotency_key,value,ex=86400)


