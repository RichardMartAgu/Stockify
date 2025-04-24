from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.utils.logger import logger
from app.models.product_model import Product
from app.models.transaction_model import Transaction
from app.models.transaction_products_midtable import transaction_products


def get_transactions(db: Session):
    try:
        data = db.query(Transaction).all()
        logger.info(f"Fetched {len(data)} transactions from the database")
        return data
    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching transactions: {str(e)}"
        )


def get_transaction_by_id(transaction_id: int, db: Session):
    try:
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            logger.warning(f"Transaction with ID {transaction_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {transaction_id} does not exist"
            )
        logger.info(f"Transaction with ID {transaction_id} fetched successfully")
        return transaction
    except Exception as e:
        logger.error(f"Error fetching transaction with ID {transaction_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching transaction: {str(e)}"
        )


def get_products_by_transaction_id(transaction_id: int, db: Session):
    try:
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            logger.warning(f"Transaction with ID {transaction_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {transaction_id} does not exist"
            )

        products = db.query(Product).join(transaction_products).filter(
            transaction_products.c.transaction_id == transaction_id).all()
        if not products:
            logger.warning(f"No products found for transaction ID {transaction_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No products found under transaction with ID {transaction_id}"
            )

        products_list = [
            {
                "product_id": product.id,
                "quantity": product.quantity
            }
            for product in products
        ]

        transaction_data = {
            "id": transaction.id,
            "identifier": transaction.identifier,
            "date": transaction.date,
            "type": transaction.type,
            "warehouse_id": transaction.warehouse_id,
            "client_id": transaction.client_id,
            "products_list": products_list
        }

        logger.info(f"Fetched products for transaction ID {transaction_id}")
        return transaction_data

    except Exception as e:
        logger.error(f"Error fetching products for transaction ID {transaction_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products for transaction: {str(e)}"
        )


def create_transaction(transaction_data, db: Session):
    try:
        logger.info("Creating new transaction")
        new_transaction = Transaction(
            identifier=transaction_data.identifier,
            type=transaction_data.type,
            date=datetime.now(timezone.utc),
            warehouse_id=transaction_data.warehouse_id,
            client_id=transaction_data.client_id
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        logger.info(f"Transaction created with ID {new_transaction.id}")

        product_entries = [
            {
                "transaction_id": new_transaction.id,
                "product_id": product.product_id,
                "quantity": product.quantity
            }
            for product in transaction_data.products
        ]

        if product_entries:
            stmt = insert(transaction_products).values(product_entries)
            db.execute(stmt)
            db.commit()
            logger.info(f"Inserted {len(product_entries)} products into transaction ID {new_transaction.id}")

        return {
            "id": new_transaction.id,
            "identifier": new_transaction.identifier,
            "date": new_transaction.date.isoformat(),
            "type": new_transaction.type,
            "warehouse_id": new_transaction.warehouse_id,
            "client_id": new_transaction.client_id,
            "products": product_entries
        }

    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating transaction: {str(e)}"
        )


def delete_transaction(transaction_id: int, db: Session):
    try:
        logger.info(f"Deleting transaction with ID {transaction_id}")
        transaction_exists = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction_exists:
            logger.warning(f"Transaction with ID {transaction_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {transaction_id} does not exist"
            )

        db.query(Transaction).filter(Transaction.id == transaction_id).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Transaction with ID {transaction_id} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting transaction with ID {transaction_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting transaction: {str(e)}"
        )
    return None
