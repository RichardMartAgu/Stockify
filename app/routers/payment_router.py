import stripe
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.repository import payment_repository
from app.utils.error_response import get_error_response

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)

@router.post("/create-checkout-session", status_code=status.HTTP_200_OK,
             description="This endpoint get Stripe checkout session.",
             responses={
                 status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
                 status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                               "You do not have access to this resource."),
                 status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                           "Internal Server Error"), })
async def create_checkout_session(user_id: int, db: Session = Depends(get_db)):
    session = payment_repository.create_checkout_session(user_id,db)
    return session