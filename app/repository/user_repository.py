from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.alert_model import Alert
from app.models.client_model import Client
from app.models.user_model import User
from app.models.warehouse_model import Warehouse
from app.utils.hashing import Hash


def get_users(db: Session):
    data = db.query(User).all()
    return data


def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )
    return user


def get_users_by_user_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )

    users = db.query(User).filter(User.admin_id == user_id).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No users found under admin with ID {user_id}"
        )

    users_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "users": users_list
    }

    return user_data


def get_warehouses_by_user_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )

    warehouses = db.query(Warehouse).filter(Warehouse.user_id == user.id).all()

    warehouses_list = [
        {
            "id": warehouse.id,
            "name": warehouse.name,
            "address": warehouse.address,
            "phone": warehouse.phone
        }
        for warehouse in warehouses
    ]

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "warehouses": warehouses_list
    }

    return user_data

def get_clients_by_user_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )

    clients = db.query(Client).filter(Client.user_id == user.id).all()

    clients_list = [
        {
            "id": warehouse.id,
            "identifier": warehouse.identifier,
            "name": warehouse.name,
            "contact": warehouse.name,
            "phone": warehouse.phone,
            "email": warehouse.email,
            "address": warehouse.address,
            "user_id": warehouse.user_id,
        }
        for warehouse in clients
    ]

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "clients": clients_list
    }

    return user_data


def get_alerts_by_user_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )

    alerts = db.query(Alert).filter(Alert.user_id == user.id).all()

    if not alerts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No alerts found under user with ID {user_id}"
        )

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

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "alerts": alerts_list
    }

    return user_data


def create_user(user, db: Session):
    user = user.dict()
    try:

        admin_id = user.get("admin_id", None)
        image_url = user.get("image_url", None)

        new_user = User(
            username=user["username"],
            password=Hash.hash_password(user["password"]),
            email=user["email"],
            role=user["role"],
            image_url=image_url,
            admin_id=admin_id,
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error create user: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create user conflict {e}"
        )


def update_user(user_id: int, user_update, db: Session):
    user = db.query(User).filter(User.id == user_id)
    user_instance = user.first()

    if not user_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )

    try:

        user_data = user_update.dict(exclude_unset=True)

        if "password" in user_data:
            user_data["password"] = Hash.hash_password(user_data["password"])

        user.update(user_data)
        db.commit()
        db.refresh(user_instance)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

    return user_instance


def delete_user(user_id: int, db: Session):
    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )
    try:
        db.query(User).filter(User.id == user_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
    return None
