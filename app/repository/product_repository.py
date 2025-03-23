from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.main import logger
from app.models.alert_model import Alert
from app.models.product_model import Product
from app.models.transaction_model import Transaction
from app.models.transaction_products_midtable import transaction_products


def get_products(db: Session):
    logger.info("Fetching all products")
    data = db.query(Product).all()
    logger.info(f"Found {len(data)} products")
    return data


def get_product_by_id(product_id: int, db: Session):
    logger.info(f"Fetching product by ID: {product_id}")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger.error(f"Product with ID {product_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )
    logger.info(f"Product found: {product.name}")
    return product


def get_products_by_product_id(product_id: int, db: Session):
    logger.info(f"Fetching products under product ID: {product_id}")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        logger.error(f"Product with ID {product_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )

    products = db.query(Product).filter(Product.kit_id == product_id).all()
    if not products:
        logger.warning(f"No products found under product with ID {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found under product with ID {product_id}"
        )

    logger.info(f"Found {len(products)} products under product ID {product_id}")
    products_list = [
        {
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "serial_number": product.serial_number,
            "price": product.price,
            "description": product.description,
            "kit_id": product.kit_id,
            "category": product.category,
            "image_url": product.image_url,
            "warehouse_id": product.warehouse_id
        }
        for product in products
    ]

    product_data = {
        "id": product.id,
        "name": product.name,
        "quantity": product.quantity,
        "serial_number": product.serial_number,
        "price": product.price,
        "description": product.description,
        "category": product.category,
        "image_url": product.image_url,
        "warehouse_id": product.warehouse_id,
        "kit_products": products_list
    }

    return product_data


def get_transactions_by_product_id(product_id: int, db: Session):
    logger.info(f"Fetching transactions for product ID: {product_id}")
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        logger.error(f"Product with ID {product_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )

    transactions = (
        db.query(Transaction)
        .join(transaction_products, transaction_products.c.transaction_id == Transaction.id)
        .filter(transaction_products.c.product_id == product.id)
        .all()
    )
    if not transactions:
        logger.warning(f"No transactions found for product ID {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No transactions found under product with ID {product_id}"
        )

    logger.info(f"Found {len(transactions)} transactions for product ID {product_id}")
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

    product_data = {
        "id": product.id,
        "name": product.name,
        "quantity": product.quantity,
        "serial_number": product.serial_number,
        "price": product.price,
        "description": product.description,
        "category": product.category,
        "image_url": product.image_url,
        "warehouse_id": product.warehouse_id,
        "transactions": transactions_list
    }

    return product_data


def get_alerts_by_product_id(product_id: int, db: Session):
    logger.info(f"Fetching alerts for product ID: {product_id}")
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        logger.error(f"Product with ID {product_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )

    alerts = db.query(Alert).filter(Alert.product_id == product.id).all()

    if not alerts:
        logger.warning(f"No alerts found for product ID {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No alerts found under product with ID {product_id}"
        )

    logger.info(f"Found {len(alerts)} alerts for product ID {product_id}")
    alerts_list = [
        {
            "id": alert.id,
            "date": alert.date,
            "read": alert.read,
            "min_quantity": alert.min_quantity,
            "max_quantity": alert.max_quantity,
            "max_message": alert.min_quantity,
            "min_message": alert.min_message,
            "product_id": alert.product_id
        }
        for alert in alerts
    ]

    product_data = {
        "id": product.id,
        "name": product.name,
        "quantity": product.quantity,
        "serial_number": product.serial_number,
        "price": product.price,
        "description": product.description,
        "category": product.category,
        "image_url": product.image_url,
        "warehouse_id": product.warehouse_id,
        "alerts": alerts_list
    }

    return product_data


def create_product(product, db: Session):
    logger.info(f"Creating new product: {product['name']}")
    product = product.dict()
    try:
        image_url = product.get("image_url", None)
        description = product.get("description", None)
        kit_id = product.get("kit_id", None)
        category = product.get("category", None)

        new_product = Product(
            name=product["name"],
            quantity=product["quantity"],
            serial_number=product["serial_number"],
            price=product["price"],
            description=description,
            kit_id=kit_id,
            category=category,
            image_url=image_url,
            warehouse_id=product["warehouse_id"],
        )

        try:
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            logger.info(f"Product {new_product.name} created successfully")
            return new_product

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating product: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error create product: {str(e)}"
            )

    except Exception as e:
        db.rollback()
        logger.error(f"Create product conflict: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create product conflict {e}"
        )


def update_product(product_id: int, product_update, db: Session):
    logger.info(f"Updating product with ID {product_id}")
    product = db.query(Product).filter(Product.id == product_id)
    product_instance = product.first()

    if not product_instance:
        logger.error(f"Product with ID {product_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )

    try:
        product.update(product_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(product_instance)
        logger.info(f"Product {product_instance.name} updated successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )

    return product_instance


def delete_product(product_id: int, db: Session):
    logger.info(f"Deleting product with ID {product_id}")
    product_exists = db.query(Product).filter(Product.id == product_id).first()
    if not product_exists:
        logger.error(f"Product with ID {product_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )
    try:
        db.query(Product).filter(Product.id == product_id).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Product with ID {product_id} deleted successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )

    return None
