from datetime import datetime, UTC

from fastapi import HTTPException, status
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.models.transaction_model import Transaction
from app.models.transaction_products_midtable import transaction_products


def get_transactions(db: Session):
    data = db.query(Transaction).all()
    return data


def get_transaction_by_id(transaction_id: int, db: Session):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} does not exist"
        )
    return transaction


def get_products_by_transaction_id(transaction_id: int, db: Session):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    products = db.query(Product).join(
        transaction_products
    ).filter(transaction_products.c.transaction_id == transaction_id).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found under admin with ID {transaction_id}"
        )

    products = [
        {
            "product_id": product.id,
            "quantity": product.quantity
        }
        for product in products
    ]

    user_data = {
        "id": transaction.id,
        "identifier": transaction.identifier,
        "date": transaction.date,
        "type": transaction.type,
        "warehouse_id": transaction.warehouse_id,
        "client_id": transaction.client_id,
        "products": products
    }

    return user_data


def create_transaction(transaction_data, db: Session):
    try:

        new_transaction = Transaction(
            identifier=transaction_data.identifier,
            type=transaction_data.type,
            date=datetime.now(UTC),
            warehouse_id=transaction_data.warehouse_id,
            client_id=transaction_data.client_id
        )

        try:

            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)

            product_entries = []
            for product in transaction_data.products:
                product_entries.append({
                    "transaction_id": new_transaction.id,
                    "product_id": product.product_id,
                    "quantity": product.quantity
                })

            if product_entries:
                stmt = insert(transaction_products).values(product_entries)
                db.execute(stmt)
                db.commit()

            new_transaction = {
                "id": new_transaction.id,
                "identifier": new_transaction.identifier,
                "date": new_transaction.date.isoformat(),
                "type": new_transaction.type,
                "warehouse_id": new_transaction.warehouse_id,
                "client_id": new_transaction.client_id,
                "products": product_entries
            }
            return new_transaction

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error create transaction: {str(e)}"
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create transaction conflict {e}"
        )


def delete_transaction(transaction_id: int, db: Session):
    transaction_exists = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with ID {transaction_id} does not exist"
        )
    try:
        db.query(Transaction).filter(Transaction.id == transaction_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting transaction: {str(e)}"
        )
    return None
