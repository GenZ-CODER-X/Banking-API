from sqlalchemy import text
from core.config import settings
from core.security import get_curent_user
from repositries.account_repositrie import Accout_repositry
from fastapi import HTTPException,status
from schemas.Account_schema import Account

def account_creation(db,account_credentials,current_user):
    user_id=current_user.id
    account_id = Accout_repositry.get_new_account_id(db)
    account_number=settings.secret_prefix_str+str(settings.secret_prefix_int+account_id)
    account_creation_details={
        "account_number":account_number,
        "user_id":user_id,
        "account_type":account_credentials.account_type,
    }
    Account_Creation=Accout_repositry.create_account(db,account_creation_details)
    return Account_Creation
