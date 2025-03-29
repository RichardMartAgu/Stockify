from datetime import datetime, UTC

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils.logger import logger
from app.models.alert_model import Alert


def get_alerts(db: Session):
    try:
        logger.info("Fetching all alerts from the database.")
        data = db.query(Alert).all()
        logger.info(f"Found {len(data)} alerts.")
        return data
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching alerts: {e}"
        )


def get_alert_by_id(alert_id: int, db: Session):
    try:
        logger.info(f"Fetching alert with ID {alert_id}.")
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            logger.warning(f"Alert with ID {alert_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert with ID {alert_id} does not exist"
            )
        logger.info(f"Alert with ID {alert_id} found.")
        return alert
    except Exception as e:
        logger.error(f"Error fetching alert with ID {alert_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching alert: {e}"
        )


def create_alert(alert, db: Session):
    alert = alert.dict()
    try:
        logger.info("Attempting to create a new alert.")

        max_quantity = alert.get("max_quantity", None)
        max_message = alert.get("max_message", None)
        min_message = alert.get("min_message", None)

        new_alert = Alert(
            date=datetime.now(UTC),
            read=alert["read"],
            min_quantity=alert["min_quantity"],
            max_quantity=max_quantity,
            max_message=max_message,
            min_message=min_message,
            product_id=alert["product_id"],
            user_id=alert["user_id"],
        )

        try:
            db.add(new_alert)
            db.commit()
            db.refresh(new_alert)
            logger.info(f"Alert with ID {new_alert.id} created successfully.")
            return new_alert
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating alert: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error create alert: {str(e)}"
            )

    except Exception as e:
        db.rollback()
        logger.error(f"Conflict creating alert: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create alert conflict {e}"
        )


def update_alert(alert_id: int, alert_update, db: Session):
    try:
        logger.info(f"Attempting to update alert with ID {alert_id}.")
        alert = db.query(Alert).filter(Alert.id == alert_id)
        alert_instance = alert.first()

        if not alert_instance:
            logger.warning(f"Alert with ID {alert_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert with ID {alert_id} does not exist"
            )

        alert.update(alert_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(alert_instance)
        logger.info(f"Alert with ID {alert_id} updated successfully.")
        return alert_instance
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating alert with ID {alert_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating alert: {str(e)}"
        )


def delete_alert(alert_id: int, db: Session):
    try:
        logger.info(f"Attempting to delete alert with ID {alert_id}.")
        alert_exists = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert_exists:
            logger.warning(f"Alert with ID {alert_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alert with ID {alert_id} does not exist"
            )

        db.query(Alert).filter(Alert.id == alert_id).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Alert with ID {alert_id} deleted successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting alert with ID {alert_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting alert: {str(e)}"
        )
    return None
