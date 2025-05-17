from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.utils.logger import logger
from app.models.product_model import Product
from app.models.transaction_model import Transaction
from app.models.transaction_products_midtable import TransactionProduct
from app.utils.identifier import generate_identifier


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

        products = db.query(Product).join(transaction.transaction_products).filter(
            transaction.transaction_products.c.transaction_id == transaction_id).all()
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
            identifier=generate_identifier(db),
            type=transaction_data.type,
            date=datetime.now(timezone.utc),
            warehouse_id=transaction_data.warehouse_id,
            client_id=transaction_data.client_id
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        logger.info(f"Transaction created with ID {new_transaction.id}, type: {transaction_data.type}")

        product_entries = []
        for product in transaction_data.products:

            product_in_db = db.query(Product).filter(Product.id == product.product_id).first()

            if not product_in_db:
                logger.warning(f"Product {product.product_id} not found")
                raise HTTPException(status_code=404, detail="Product not found")

            if transaction_data.type == 'out':
                logger.info(
                    f"Trying to remove {product.quantity} units from product {product.product_id} (current stock: {product_in_db.quantity})")
                if product_in_db.quantity < product.quantity:
                    logger.error(
                        f"Insufficient stock for product {product.product_id}: available {product_in_db.quantity}, required {product.quantity}")
                    raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.product_id}")
                product_in_db.quantity -= product.quantity
                logger.info(
                    f"New stock for product {product.product_id} after outgoing transaction: {product_in_db.quantity}")

            elif transaction_data.type == 'in':
                logger.info(
                    f"Adding {product.quantity} units to product {product.product_id} (current stock: {product_in_db.quantity})")
                product_in_db.quantity += product.quantity
                logger.info(
                    f"New stock for product {product.product_id} after incoming transaction: {product_in_db.quantity}")

            db.add(product_in_db)

            product_entries.append({
                "transaction_id": new_transaction.id,
                "product_id": product.product_id,
                "quantity": product.quantity
            })

        if product_entries:
            stmt = insert(TransactionProduct).values(product_entries)
            db.execute(stmt)

        db.commit()
        logger.info(f"Transaction completed with {len(product_entries)} products")

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
