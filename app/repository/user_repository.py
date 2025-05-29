from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils.logger import logger
from app.models.alert_model import Alert
from app.models.client_model import Client
from app.models.user_model import User
from app.models.warehouse_model import Warehouse
from app.utils.hashing import Hash


def get_users(db: Session):
    try:
        data = db.query(User).all()
        logger.info(f"Fetched {len(data)} users from the database")
        return data
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )


def get_user_by_id(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} does not exist"
            )
        logger.info(f"User with ID {user_id} fetched successfully")
        return user
    except Exception as e:
        logger.error(f"Error fetching user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )


def get_users_by_user_id(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} does not exist"
            )

        users = db.query(User).filter(User.admin_id == user_id).all()

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

        logger.info(f"Fetched users under admin with ID {user_id}")
        return user_data
    except Exception as e:
        logger.error(f"Error fetching users under admin with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )


def get_clients_by_user_id(user_id: int, db: Session):
    try:
        logger.info(f"Fetching user with ID {user_id}")
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} does not exist"
            )

        logger.info(f"User with ID {user_id} found. Fetching clients...")
        clients = db.query(Client).filter(Client.user_id == user.id).all()

        clients_list = [
            {
                "id": client.id,
                "identifier": client.identifier,
                "name": client.name,
                "contact": client.contact,
                "phone": client.phone,
                "email": client.email,
                "address": client.address,
                "user_id": client.user_id,
            }
            for client in clients
        ]

        logger.info(f"Fetched {len(clients_list)} clients for user ID {user_id}")

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "clients": clients_list
        }

        return user_data
    except Exception as e:
        logger.error(f"Error fetching clients for user ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching clients: {str(e)}"
        )


def get_warehouses_by_user_id(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User with ID {user_id} not found")
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

        logger.info(f"Fetched warehouses under user with ID {user_id}")
        return user_data
    except Exception as e:
        logger.error(f"Error fetching warehouses under user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching warehouses: {str(e)}"
        )


def get_alerts_by_user_id(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} does not exist"
            )

        alerts = db.query(Alert).filter(Alert.user_id == user.id).all()

        if not alerts:
            logger.warning(f"No alerts found under user with ID {user_id}")
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
                "max_message": alert.max_message,
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

        logger.info(f"Fetched alerts under user with ID {user_id}")
        return user_data
    except Exception as e:
        logger.error(f"Error fetching alerts under user with ID {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching alerts: {str(e)}"
        )


def create_user(user, db: Session):
    user = user.dict()

    if db.query(User).filter(User.email == user["email"]).first():
        logger.error(f"Error creating user: Email already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if db.query(User).filter(User.username == user["username"]).first():
        logger.error(f"Error creating user: Username already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    try:
        logger.info("Creating new user")

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

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User created with ID {new_user.id}")
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


def update_user(user_id: int, user_update, db: Session):
    user = db.query(User).filter(User.id == user_id)
    user_instance = user.first()

    if not user_instance:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )

    existing_username = db.query(User).filter(
        User.name == user_update.name,
        User.id != user_id
    ).first()

    if existing_username:
        logger.error(f"Error creating User: Name already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name already registered"
        )

    existing_user_email = db.query(User).filter(
        User.email == user_update.email,
        User.id != user_id
    ).first()

    if existing_username:
        logger.error(f"Error creating User: Email already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:

        user_data = user_update.dict(exclude_unset=True)

        if "password" in user_data:
            user_data["password"] = Hash.hash_password(user_data["password"])

        user.update(user_data)
        db.commit()
        db.refresh(user_instance)
        logger.info(f"User with ID {user_id} updated successfully")
        return user_instance
    except Exception as e:
        logger.error(f"Error updating user with ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


def delete_user(user_id: int, db: Session):
    try:
        user_exists = db.query(User).filter(User.id == user_id).first()
        if not user_exists:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} does not exist"
            )

        db.query(User).filter(User.id == user_id).delete(synchronize_session=False)
        db.commit()
        logger.info(f"User with ID {user_id} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )
    return None
