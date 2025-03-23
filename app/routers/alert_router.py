from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.main import logger
from app.repository import alert_repository
from app.schemas.alert_schema import UpdateAlertSchema, CreateAlertSchema, AlertResponseSchema
from app.schemas.token_schema import TokenData
from app.utils.error_response import get_error_response
from app.utils.oauth import role_required

router = APIRouter(
    prefix="/alert",
    tags=["Alert"]
)


@router.get('/', response_model=List[AlertResponseSchema], status_code=status.HTTP_200_OK,
            description="This endpoint is available to Admin alerts.",
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error"), })
def get_alerts(db: Session = Depends(get_db),
               current_alert: TokenData = Depends(role_required(['Admin']))):
    logger.info("[ROUTER] Fetching all alerts.")
    alerts_data = alert_repository.get_alerts(db)
    logger.info(f"[ROUTER] Fetched {len(alerts_data)} alerts.")
    return alerts_data


@router.get('/{alert_id}', response_model=AlertResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Alert with ID {alert_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_alert_by_id(alert_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching alert with ID {alert_id}.")
    alert = alert_repository.get_alert_by_id(alert_id, db)
    logger.info(f"[ROUTER] Found alert: {alert} with ID {alert_id}.")
    return alert


@router.post('/', response_model=AlertResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create alert error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_alert(alert: CreateAlertSchema, db: Session = Depends(get_db)):
    logger.info("[ROUTER] Creating new alert.")
    created_alert = alert_repository.create_alert(alert, db)
    logger.info(f"[ROUTER] Alert created: {created_alert}")
    return created_alert


@router.put('/{alert_id}', response_model=AlertResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Alert with ID {alert_id} does not exist"),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Update alert error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def update_alert(alert_id: int, alert: UpdateAlertSchema, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Updating alert with ID {alert_id}.")
    edited_alert = alert_repository.update_alert(alert_id, alert, db)
    logger.info(f"[ROUTER] Alert with ID {alert_id} updated: {edited_alert}.")
    return edited_alert


@router.delete('/{alert_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Alert with ID {alert_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Deleting alert with ID {alert_id}.")
    alert_repository.delete_alert(alert_id, db)
    logger.info(f"[ROUTER] Alert with ID {alert_id} deleted.")
    return None
