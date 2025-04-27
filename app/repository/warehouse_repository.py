from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.product_model import Product
from app.models.transaction_model import Transaction
from app.models.transaction_products_midtable import TransactionProduct
from app.models.warehouse_model import Warehouse
from app.utils.logger import logger


def get_warehouses(db: Session):
    logger.info("Fetching all warehouses from the database.")
    data = db.query(Warehouse).all()
    logger.info(f"Retrieved {len(data)} warehouses.")
    return data


def get_warehouse_by_id(warehouse_id: int, db: Session):
    logger.info(f"Fetching warehouse with ID {warehouse_id} from the database.")
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        logger.error(f"Warehouse with ID {warehouse_id} does not exist.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )
    logger.info(f"Warehouse with ID {warehouse_id} found.")
    return warehouse

def get_products_by_warehouse_id(warehouse_id: int, db: Session):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )

    products = db.query(Product).filter(Product.warehouse_id == warehouse.id).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found under warehouse with ID {warehouse_id}"
        )

    products = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category": product.category,
            "image_url": product.image_url
        }
        for product in products
    ]

    warehouse_data = {
        "id": warehouse.id,
        "name": warehouse.name,
        "address": warehouse.address,
        "phone": warehouse.phone,
        "user_id": warehouse.user_id,
        "products": products
    }

    return warehouse_data




def get_transactions_by_warehouse_id(warehouse_id: int, db: Session):
    logger.info(f"Fetching transactions for warehouse with ID {warehouse_id}.")
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    if not warehouse:
        logger.error(f"Warehouse with ID {warehouse_id} does not exist.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )

    transactions = db.query(Transaction) \
        .filter(Transaction.warehouse_id == warehouse.id) \
        .options(joinedload(Transaction.transaction_products).joinedload(TransactionProduct.product)) \
        .all()

    logger.info(f"Found {len(transactions)} transactions for warehouse ID {warehouse_id}.")

    transactions_list = []
    for transaction in transactions:
        products_list = []
        for tp in transaction.transaction_products:
            products_list.append({
                "quantity": tp.quantity,
                "product": {
                    "id": tp.product.id,
                    "name": tp.product.name,
                    "quantity": tp.product.quantity,
                    "serial_number": tp.product.serial_number,
                    "price": tp.product.price,
                    "description": tp.product.description,
                    "category": tp.product.category,
                    "image_url": tp.product.image_url,
                    "kit_id": tp.product.kit_id,
                    "warehouse_id": tp.product.warehouse_id,
                }
            })

        transactions_list.append({
            "id": transaction.id,
            "identifier": transaction.identifier,
            "date": transaction.date,
            "type": transaction.type,
            "warehouse_id": transaction.warehouse_id,
            "client_id": transaction.client_id,
            "products": products_list
        })

    warehouse_data = {
        "id": warehouse.id,
        "name": warehouse.name,
        "address": warehouse.address,
        "phone": warehouse.phone,
        "user_id": warehouse.user_id,
        "transactions": transactions_list,
    }

    return warehouse_data

def create_warehouse(warehouse, db: Session):
    logger.info("Creating a new warehouse.")
    warehouse = warehouse.dict()
    try:

        address = warehouse.get("address", None)
        phone = warehouse.get("phone", None)
        user_id = warehouse.get("user_id", None)

        new_warehouse = Warehouse(
            name=warehouse["name"],
            address=address,
            phone=phone,
            user_id=user_id,
        )

        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)
        logger.info(f"Warehouse with ID {new_warehouse.id} created successfully.")
        return new_warehouse

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating warehouse: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error create warehouse: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create warehouse conflict {str(e)}"
        )

def update_warehouse(warehouse_id: int, warehouse_update, db: Session):
    logger.info(f"Updating warehouse with ID {warehouse_id}.")
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id)
    warehouse_instance = warehouse.first()

    if not warehouse_instance:
        logger.error(f"Warehouse with ID {warehouse_id} does not exist.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )

    try:
        warehouse.update(warehouse_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(warehouse_instance)
        logger.info(f"Warehouse with ID {warehouse_id} updated successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating warehouse: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating warehouse: {str(e)}"
        )

    return warehouse_instance

def delete_warehouse(warehouse_id: int, db: Session):
    logger.info(f"Deleting warehouse with ID {warehouse_id}.")
    warehouse_exists = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_exists:
        logger.error(f"Warehouse with ID {warehouse_id} does not exist.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )

    try:
        db.query(Warehouse).filter(Warehouse.id == warehouse_id).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Warehouse with ID {warehouse_id} deleted successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting warehouse: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting warehouse: {str(e)}"
        )

    return None
