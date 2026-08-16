from fastapi import HTTPException,status
from repositries.account_repositrie import Accout_repositry
from core.security import settings
from repositries.Transaction_repositries import Transaction_repositry
from repositries.redis_repositries import RedisRepository

def transaction(db,Current_user,transaction_details,idempotency_key):
    redis_repository = RedisRepository()
    cached_response=redis_repository.get_response(idempotency_key)
    if cached_response:
        return cached_response
    try:
        if transaction_details.amount<=0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The amount trying to send is invalid")
        sender_acc=Accout_repositry.get_account_for_update(db,Current_user.user_id)
        if sender_acc.status=="Frozen":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Your account is freezed")
        if sender_acc.balance<transaction_details.amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=F"Balance is insuffiecient")
        receiver_acc=Accout_repositry.get_account_for_update(db,transaction_details.Receiver_acc_no)
       
        if receiver_acc is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Receiver not found")
        
        if receiver_acc.status=="Frozen":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"The receiver acc is frozen")

        if sender_acc.id==receiver_acc.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Cant transfer to the same user")

        balance_sender=sender_acc.balance-transaction_details.amount
        balance_receiver=receiver_acc.balance+transaction_details.amount
        Transaction_repositry.balance_updated(db,balance_sender,sender_acc)
        Transaction_repositry.balance_updated(db,balance_receiver,receiver_acc)
        transaction_id=Transaction_repositry.transaction_id(db)

        Transaction_Ref=settings.secret_prefix_transaction+str(settings.secret_prefix_int+transaction_id)

        transaction_entry_data={
            "amount":transaction_details.amount,
            "Transaction_Ref":Transaction_Ref,
            "Sender_ACC_id":sender_acc.id,
            "Receiver_ACC_id":receiver_acc.id,
            "description":transaction_details.description,
        }
        transaction_request=Transaction_repositry.transaction_entry(db,transaction_entry_data)
        create_ledger_entry={
            "account_id":sender_acc.id,
            "transaction_id":transaction_request.id,
            "amount":transaction_details.amount,
        }
        Transaction_repositry.ledger_entry(db,create_ledger_entry,"Debited",sender_acc)
        Transaction_repositry.ledger_entry(db,create_ledger_entry,"Credited",receiver_acc)
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Transaction failed no money is deducted")
    Transaction_response={
            "amount":transaction_details.amount,
            "transaction_ref":Transaction_Ref,
            "status":"SUCCESSFUL"
        }
    redis_repository.save_response(idempotency_key,Transaction_response)
    return Transaction_response

def get_transaction_history(db,user_id):
    Transactions=Transaction_repositry.get_transaction_for_user(db,user_id)
    if Transactions is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not registered")
    if not Transactions:
        return []
    else:
        return Transactions


    
    
