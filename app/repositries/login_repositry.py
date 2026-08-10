from app.models.refresh_sessions import RefreshSession
from sqlalchemy import text

class LoginRepositry():
    def search_refresh_token(db,refresh_token):
        User=db.query(RefreshSession).filter(RefreshSession.refresh_token_hash==refresh_token).first()
        return User
    
    def update_refresh_token(db,Refresh_session,new_refresh_token,new_expire_time):
        Refresh_session.refresh_token_hash=new_refresh_token
        Refresh_session.expires_at=new_expire_time
        
    def delete_refresh_token(db,refresh_token):
        session = db.query(RefreshSession).filter(RefreshSession.refresh_token_hash==refresh_token).first()
        db.delete(session)

    def refresh_token_to_db(db,refresh_token):
        new_refresh_token_query=RefreshSession(**refresh_token)
        db.add(new_refresh_token_query)
