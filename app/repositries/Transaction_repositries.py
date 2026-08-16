from app.models.transactions import Transaction
from app.models.accounts import Account
from sqlalchemy import text
from app.models.ledger import Ledger
from sqlalchemy import or_
from sqlalchemy.orm import aliased

class Transaction_repositry():
    def transaction_id(db):
        transaction_id = db.execute(
    text("SELECT nextval('transaction_number_sequence')")
).scalar_one()
        return transaction_id
    
    def transaction_entry(db,transaction_details):
        transanction_entry_query=Transaction(**transaction_details)
        db.add(transanction_entry_query)
        db.flush()
        return transanction_entry_query
    
    def ledger_entry(db,ledger_entry,transaction_type,account):
        ledger_entry["transaction_type"]=transaction_type
        if transaction_type=="DEBIT":
            ledger_entry["account_id"]=account.id
        ledger_entry_query=Ledger(**ledger_entry)
        db.add(ledger_entry_query)

    def balance_updated(db,amount,Account):
        Account.balance=amount
    
    def transaction_status_update(db,transaction_id):
        transaction_query=db.query(Transaction).filter(Transaction.id==transaction_id).first()
        transaction_query.update(Transaction.status=="Successful")
        
    def get_transactions_for_user(db,user_id):
        User_acc=db.query(Account).filter(Account.user_id==user_id).first()
        if User_acc is None:
            return None
        User_acc_id=User_acc.id
        SenderAccount = aliased(Account)
        ReceiverAccount = aliased(Account)
        transactions = (
    db.query(Transaction)
    .join(
        SenderAccount,
        Transaction.Sender_ACC_id == SenderAccount.id
    )
)
        transactions_of_user=db.query(Transaction).filter(or_(Transaction.Sender_ACC_id==User_acc_id ,
                                                              Transaction.Receiver_ACC_id==User_acc_id)).all()
        if transactions_of_user is None:
            return 1
        return transactions_of_user
