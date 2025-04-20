from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.utils.hashing import Hash
from app.utils.token import create_access_token


def auth_user(user, db: Session):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no user with the username {user.username}, login is not possible."
        )

    if not Hash.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )
    access_token = create_access_token(
        data={"sub": user.username, "role": db_user.role}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": db_user.id,
        "username": db_user.username,
        "email":db_user.email,
        "image_url": db_user.image_url,

    }
