import os
from http.client import HTTPException

import stripe
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.models import User

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def process_webhook_event(event, db: Session):
    if event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        subscription_id = invoice.get("subscription")
        customer_id = invoice.get("customer")

        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()

        if user:
            user.stripe_subscription_id = subscription_id
            user.stripe_subscription_status = "active"
            db.commit()

            return JSONResponse(status_code=200, content={"message": "Successfully payment"})
        else:
            return JSONResponse(status_code=404, content={"error": "User not found"})

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        customer_id = subscription.get("customer")
        subscription_status = subscription.get("status")

        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()

        if user:
            if subscription_status == "active":
                user.stripe_subscription_id = subscription.get("id")
                user.stripe_subscription_status = "active"
            elif subscription_status == "canceled":
                user.stripe_subscription_status = "canceled"

            db.commit()
            return JSONResponse(status_code=200, content={"message": "Payment subscription edited"})
        else:
            return JSONResponse(status_code=404, content={"error": "User not found"})

    else:
        return JSONResponse(status_code=400, content={"error": "Unrecognized event"})


def create_checkout_session(user_id, db):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.username
        )
        user.stripe_customer_id = customer.id
        db.commit()

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Suscripción trimestral a Stripe",
                    },
                    "unit_amount": 2000,
                },
                "quantity": 1,
            }],
            success_url="http://localhost:3000/payment/success",
            cancel_url="http://localhost:3000/payment/fail",
            customer=user.stripe_customer_id,
        )
        return {"sessionId": session.id}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
