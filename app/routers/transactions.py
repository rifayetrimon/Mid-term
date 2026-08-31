from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models import Transaction, User
from app.schemas import TransactionCreate, TransactionOut

router = APIRouter(prefix="/transactions", tags=["transactions"])


def find_transaction(db, transaction_id, user):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.owner_id == user.id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    new_transaction = Transaction(
        title=data.title,
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date,
        owner_id=user.id,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@router.get("", response_model=list[TransactionOut])
def get_all_transactions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return db.query(Transaction).filter(Transaction.owner_id == user.id).all()


@router.get("/filter", response_model=list[TransactionOut])
def filter_transactions(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    minimum_amount: Optional[float] = Query(None),
    maximum_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(Transaction).filter(Transaction.owner_id == user.id)

    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category == category)
    if minimum_amount is not None:
        query = query.filter(Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(Transaction.amount <= maximum_amount)

    return query.all()


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return find_transaction(db, transaction_id, user)


@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: int,
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    transaction = find_transaction(db, transaction_id, user)

    transaction.title = data.title
    transaction.amount = data.amount
    transaction.type = data.type
    transaction.category = data.category
    transaction.date = data.date

    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    transaction = find_transaction(db, transaction_id, user)
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
