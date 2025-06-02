import os
from http.client import HTTPException

import stripe
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.utils.logger import logger

from app.models import User

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def process_webhook_event(payload, sig_header, secret, db: Session):
    try:
        logger.info("Starting to process Stripe webhook event")
        event = stripe.Webhook.construct_event(
            payload, sig_header, secret
        )
        logger.info(f"Received event type: {event['type']}")

        if event["type"] == "invoice.payment_succeeded":
            invoice = event["data"]["object"]
            customer_id = invoice.get("customer")
            logger.info(f"Payment succeeded for customer: {customer_id}")

            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()

            if user:
                user.stripe_subscription_status = True
                db.commit()
                logger.info(f"Updated subscription status to True for user_id: {user.id}")
                return JSONResponse(status_code=200, content={"message": "Successfully payment"})
            else:
                logger.warning(f"User with customer_id {customer_id} not found")
                return JSONResponse(status_code=404, content={"error": "User not found"})

        elif event["type"] == "customer.subscription.updated":
            subscription = event["data"]["object"]
            customer_id = subscription.get("customer")
            subscription_status = subscription.get("status")
            logger.info(f"Subscription updated for customer: {customer_id}, new status: {subscription_status}")

            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()

            if user:
                if subscription_status == "active":
                    user.stripe_subscription_id = subscription.get("id")
                    user.stripe_subscription_status = True
                    logger.info(f"Set subscription active for user_id: {user.id}")
                elif subscription_status == "canceled":
                    user.stripe_subscription_status = False
                    logger.info(f"Set subscription canceled for user_id: {user.id}")

                db.commit()
                return JSONResponse(status_code=200, content={"message": "Payment subscription edited"})
            else:
                logger.warning(f"User with customer_id {customer_id} not found")
                return JSONResponse(status_code=404, content={"error": "User not found"})

        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            customer_id = subscription.get("customer")
            logger.info(f"Subscription deleted for customer: {customer_id}")

            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.stripe_subscription_status = False
                logger.info(f"Set subscription canceled for user_id: {user.id} (deleted event)")
                db.commit()
            else:
                logger.warning(f"No user found with stripe_customer_id={customer_id} on deleted event")
        else:
            logger.warning(f"Unrecognized event type: {event['type']}")
            return JSONResponse(status_code=400, content={"error": "Unrecognized event"})

    except Exception as e:
        logger.error(f"Exception processing webhook event: {e}")
        return JSONResponse(status_code=400, content={"error": "Webhook processing error"})


def create_checkout_session(user_id, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"User with id {user_id} not found when creating checkout session")
        raise HTTPException(status_code=404, detail="User not found")

    if not user.stripe_customer_id:
        logger.info(f"Creating new Stripe customer for user_id: {user.id}")
        customer = stripe.Customer.create(
            email=user.email,
            name=user.username
        )
        user.stripe_customer_id = customer.id
        db.commit()
        logger.info(f"Stripe customer created with id: {customer.id}")

    try:
        logger.info(f"Creating checkout session for user_id: {user.id}")
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": "price_1RNUKjEEie4OqAPDikNRj4lS",
                "quantity": 1,
            }],
            success_url="http://107.22.235.180/?from=success",
            cancel_url="http://107.22.235.180/?from=fail",
            customer=user.stripe_customer_id,
        )
        logger.info(f"Checkout session created with id: {session.id}")
        return {"sessionId": session.id}
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        return JSONResponse(status_code=400, content={"error": str(e)})
