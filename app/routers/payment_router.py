import os

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status

from app.utils.logger import logger
from app.db.database import get_db
from app.repository import payment_repository
from app.repository.payment_repository import process_webhook_event
from app.utils.error_response import get_error_response

webhook_key = os.getenv('STRIPE_SECRET_WEBHOOK_KEY')

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
    logger.info(f"[ROUTER] Start create checkout session")
    session = payment_repository.create_checkout_session(user_id, db)
    logger.info(f"[ROUTER] Create checkout session end.")
    return session


@router.post("/webhook", status_code=status.HTTP_200_OK,
             description="This endpoint get Stripe checkout session.",
             responses={
                 status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
                 status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                               "You do not have access to this resource."),
                 status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                           "Internal Server Error"), })
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Start get stripe webhook")
    logger.info("Received Stripe webhook request")
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    process_webhook_event(payload, sig_header, webhook_key, db)
    logger.info(f"[ROUTER] Stripe webhook end.")
    return None
