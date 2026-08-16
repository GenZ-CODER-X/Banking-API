from fastapi import HTTPException,status
from repositries.account_repositrie import Accout_repositry
from core.security import settings
from repositries.Transaction_repositries import Transaction_repositry
from repositries.redis_repositries import RedisRepository
from repositries.audit_repositry import Audit_repositry
from schemas.transactions_schemas import TransactionHistoryResponse

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

        Audit_entry_details={
        "user_id":Current_user.user_id,
        "transaction_id":transaction_request.id,
        "action":"Transfer of Amount",
        "description":transaction_details.description,
    }
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

def get_transaction_history(db,user):
    Transaction_details=Transaction_repositry.get_transactions_for_user(db,user.id)
    responses=[]
    for transaction, sender_account_no, receiver_account_no in Transaction_details:
        response=TransactionHistoryResponse(
            Transaction_Ref=transaction.Transaction_Ref,
            amount=transaction.amount,
            sender_account_no=sender_account_no,
            receiver_account_no=receiver_account_no,
            status=transaction.status,
            description=transaction.description,
            created_at=transaction.created_at
        )
        responses.append(response)
    return responses

def reconcile_ledger(db):
    total_credit,total_debit=Transaction_repositry.ledger_data
    return {
    "total_debit": total_debit,
    "total_credit": total_credit,
    "balanced": total_debit == total_credit
}




    



    
    
