from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product_model import Product


def get_products(db: Session):
    data = db.query(Product).all()
    return data


def get_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )
    return product


def create_product(product, db: Session):
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
            return new_product
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error create product: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create product error {e}"
        )


def delete_product(product_id: int, db: Session):
    product_exists = db.query(Product).filter(Product.id == product_id).first()
    if not product_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )
    try:
        db.query(Product).filter(Product.id == product_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )
    return None


def update_product(product_id: int, product_update, db: Session):
    product = db.query(Product).filter(Product.id == product_id)
    product_instance = product.first()

    if not product_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} does not exist"
        )

    try:
        product.update(product_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(product_instance)  # Refresca los datos después del commit
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )

    return product_instance
