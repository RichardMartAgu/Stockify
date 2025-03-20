from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.user_model import User
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
            detail=f"Create user error {e}"
        )


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


def update_user(user_id: int, user_update, db: Session):
    user = db.query(User).filter(User.id == user_id)
    user_instance = user.first()

    if not user_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )

    try:
        user.update(user_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(user_instance)  # Refresca los datos después del commit
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

    return user_instance
