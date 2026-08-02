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
    
    def refresh_token_check(self,refresh_token):
        response=redis_client.get(refresh_token)
        if response is None:
            return True
        return False
    
    def blacklist_refresh_token(self,refreshtoken,user_id):
        redis_client.set(refreshtoken,user_id,ex=86400)
        
