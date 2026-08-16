from app.models.accounts import Account
from sqlalchemy import text,or_

class Accout_repositry():
    def get_account_by_user_id(db,user_id):
        Current_User_Account=db.query(Account).filter(Account.user_id==user_id).first()
        return Current_User_Account
            
    def get_new_account_id(db):
        account_id = db.execute(
    text("SELECT nextval('account_number_sequence')")
).scalar_one()
        return account_id
    def get_account_by_acc_no(db,acc_no):
        Current_User_Account=db.query(Account).filter(Account.account_number==acc_no).first()
        return Current_User_Account
    
    def create_account(db,acc_details):
        new_account_query=Account(**acc_details.model_dump())
        db.add(new_account_query)
        db.commit()
        db.refresh(new_account_query)
        return new_account_query
    
    #We created this to avoid race condition by using row locking
    def get_account_for_update(db,acc_no):
        return (
        db.query(Account)
      .filter(Account.account_number == acc_no)
      .with_for_update()
      .first()
)
    def get_user_account_for_update(db, user_id):
        return (
        db.query(Account)
        .filter(Account.user_id == user_id)
        .with_for_update()
        .first()
    )

    def get_accounts_for_transfer(db, user_id, receiver_acc_no):
        accounts = (
            db.query(Account)
            .filter(
                or_(
                    Account.user_id == user_id,
                    Account.account_number == receiver_acc_no
                )
            )
            .order_by(Account.id)
            .with_for_update()
            .all()
        )
        return accounts


