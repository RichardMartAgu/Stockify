from datetime import datetime, UTC

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.alert_model import Alert


def get_alerts(db: Session):
    data = db.query(Alert).all()
    return data


def get_alert_by_id(alert_id: int, db: Session):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID {alert_id} does not exist"
        )
    return alert


def create_alert(alert, db: Session):
    alert = alert.dict()
    try:

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
            return new_alert
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error create alert: {str(e)}"
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create alert conflict {e}"
        )


def update_alert(alert_id: int, alert_update, db: Session):
    alert = db.query(Alert).filter(Alert.id == alert_id)
    alert_instance = alert.first()

    if not alert_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID {alert_id} does not exist"
        )

    try:
        alert.update(alert_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(alert_instance)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating alert: {str(e)}"
        )

    return alert_instance


def delete_alert(alert_id: int, db: Session):
    alert_exists = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID {alert_id} does not exist"
        )
    try:
        db.query(Alert).filter(Alert.id == alert_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting alert: {str(e)}"
        )
    return None
