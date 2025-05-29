import os

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status

from app.db.database import get_db
from app.repository import payment_repository
from app.repository.payment_repository import process_webhook_event
from app.schemas.payment_schema import CheckoutSessionResponse
from app.utils.error_response import get_error_response
from app.utils.logger import logger

webhook_key = os.getenv('STRIPE_SECRET_WEBHOOK_KEY')

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)


@router.post("/create-checkout-session", response_model=CheckoutSessionResponse, status_code=status.HTTP_200_OK,
             description="This endpoint get Stripe checkout session.",
             responses={
                 status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                  "Not authenticated or invalid role provided"),
                 status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                               "You do not have access to this resource."),
                 status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                           "Internal Server Error"), })
async def create_checkout_session(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Start create checkout session")
    session = payment_repository.create_checkout_session(user_id, db)
    logger.info(f"[ROUTER] Create checkout session end.")
    return session


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT,
             description="This endpoint handles incoming Stripe webhook events.",
             responses={
                 status.HTTP_400_BAD_REQUEST: get_error_response("ERROR: BAD REQUEST",
                                                                 "Invalid or missing Stripe signature."),
                 status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY",
                                                                          "Malformed webhook payload."),
                 status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                           "Internal Server Error"),
             })
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Start get stripe webhook")
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    process_webhook_event(payload, sig_header, webhook_key, db)
    logger.info(f"[ROUTER] Stripe webhook end.")
    return None
