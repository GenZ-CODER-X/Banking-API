from fastapi import HTTPException,status
from models.user import User
class UserRepositry:
    def get_by_email(db,email):
        User_query=db.query(User).filter(User.email==email).first()
        if User_query is None:
            return None
        else:
            return User_query
    # Return user if exsists or none
        pass
    def get_by_ph_no(db,ph_no):
        User_query=db.query(User).filter(User.phone_number==ph_no).first()
        if User_query is None:
            return None
        else:
            return User_query
    def get_user_by_user_id(db,id):
        Current_User=db.query(User).filter(User.id==id).first()
        if Current_User is None:
            return None
        else:
            return Current_User
        
    # Return user if exsists or none
    def create_user(db,user_details):
        new_user=User(**user_details.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    def mark_email_verified(db,user_id):
        User=db.query(User).filter(User.id==user_id).first()
        User.is_verified=True

    def reset_password(db,new_password_hashed,user_id):
        Current_User=db.query(User).filter(User.id==user_id).first()
        if Current_User is None:
            raise HTTPException(
        status_code=404,
        detail="User not found"
    )
        Current_User.password_hash=new_password_hashed
