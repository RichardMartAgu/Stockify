from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils.logger import logger
from app.models.user_model import User
from app.utils.hashing import Hash
from app.utils.token import create_access_token


def auth_user(user, db: Session):
    try:
        logger.info(f"Attempting to authenticate user with username: {user.username}")
        db_user = db.query(User).filter(User.username == user.username).first()

        if not db_user:
            logger.warning(f"User with username {user.username} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no user with the username {user.username}, login is not possible."
            )

        if not Hash.verify_password(user.password, db_user.password):
            logger.warning(f"Incorrect password attempt for user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect password"
            )
        access_token = create_access_token(
            data={"sub": user.username, "role": db_user.role}
        )
        logger.info(f"User {user.username} authenticated successfully.")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "image_url": db_user.image_url,
        }

    except Exception as e:
        logger.error(f"Error during authentication process: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )



