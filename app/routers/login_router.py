from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repository import auth_repository
from app.schemas.token_schema import TokenResponse
from app.utils.error_response import get_error_response

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


@router.post('/', response_model=TokenResponse, status_code=status.HTTP_200_OK, responses={
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create token error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def login(usuario: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_token = auth_repository.auth_user(usuario, db)
    return auth_token
