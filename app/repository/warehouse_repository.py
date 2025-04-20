from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.models.transaction_model import Transaction
from app.models.warehouse_model import Warehouse


def get_warehouses(db: Session):
    data = db.query(Warehouse).all()
    return data


def get_warehouse_by_id(warehouse_id: int, db: Session):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )
    return warehouse


def get_products_by_warehouse_id(warehouse_id: int, db: Session):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )

    products = db.query(Product).filter(Product.warehouse_id == warehouse.id).all()

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
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )

    transactions = db.query(Transaction).filter(Transaction.warehouse_id == warehouse.id).all()

    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No transactions found under warehouse with ID {warehouse_id}"
        )

    transactions_list = [
        {
            "id": transaction.id,
            "date": transaction.date,
            "type": transaction.type,
            "warehouse_id": transaction.warehouse_id,
            "client_id": transaction.client_id
        }
        for transaction in transactions
    ]

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

        try:
            db.add(new_warehouse)
            db.commit()
            db.refresh(new_warehouse)
            return new_warehouse
        except Exception as e:
            db.rollback()
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
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id)
    warehouse_instance = warehouse.first()

    if not warehouse_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )

    try:
        warehouse.update(warehouse_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(warehouse_instance)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating warehouse: {str(e)}"
        )

    return warehouse_instance


def delete_warehouse(warehouse_id: int, db: Session):
    warehouse_exists = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse with ID {warehouse_id} does not exist"
        )
    try:
        db.query(Warehouse).filter(Warehouse.id == warehouse_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting warehouse: {str(e)}"
        )
    return None
