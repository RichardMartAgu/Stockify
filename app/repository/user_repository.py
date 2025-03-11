from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserResponseSchema
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


def create_user(user, db: Session):
    user = user.dict()
    try:

        admin_id = user.get("admin_id", None)

        new_user = User(
            username=user["username"],
            password=Hash.hash_password(user["password"]),
            email=user["email"],
            role=user["role"],
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
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist"
        )
    try:
        user.update(user_update.dict(exclude_unset=True))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error update user: {str(e)}"
        )
    updated_user = db.query(User).filter(User.id == user_id).first()
    return updated_user
