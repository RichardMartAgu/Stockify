from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
import logging

from app.models.transaction_model import Transaction

logger = logging.getLogger(__name__)

def generate_identifier(db: Session) -> str:
    now = datetime.now()
    year_month = now.strftime("%Y/%m")
    prefix = f"TRAN-{year_month}-"

    logger.info(f"Generating identifier with prefix '{prefix}'")

    last_transaction = (
        db.query(Transaction)
        .filter(Transaction.identifier.like(f"{prefix}%"))
        .order_by(desc(Transaction.identifier))
        .first()
    )

    if last_transaction and last_transaction.identifier:
        try:
            last_number = int(last_transaction.identifier.split("-")[-1])
            logger.info(f"Last identifier found: {last_transaction.identifier} -> Counter: {last_number}")
            new_number = last_number + 1
        except ValueError:
            logger.warning(f"Could not parse last identifier number from: {last_transaction.identifier}")
            new_number = 1
    else:
        logger.info("No previous identifier found for this month. Starting at 1.")
        new_number = 1

    new_identifier = f"{prefix}{new_number:04d}"
    logger.info(f"Generated new identifier: {new_identifier}")
    return new_identifier
