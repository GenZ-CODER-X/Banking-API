from models.transactions import Transaction
from sqlalchemy import text
from models.ledger import Ledger

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
        
    