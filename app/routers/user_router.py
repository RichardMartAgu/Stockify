from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.main import logger
from app.repository import user_repository
from app.schemas.token_schema import TokenData
from app.schemas.user_schema import UpdateUserSchema, CreateUserSchema, UserResponseSchema, UserEmployeesResponseSchema, \
    UserWarehousesResponseSchema, UserAlertsResponseSchema
from app.utils.error_response import get_error_response
from app.utils.oauth import role_required

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get('/', response_model=List[UserResponseSchema], status_code=status.HTTP_200_OK,
            description="This endpoint is available to Admin users.",
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error"), })
def get_users(db: Session = Depends(get_db),
              current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info("[ROUTER] Fetching all users.")
    users_data = user_repository.get_users(db)
    logger.info(f"[ROUTER] Fetched {len(users_data)} users.")
    return users_data


@router.get('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching user with ID {user_id}.")
    user = user_repository.get_user_by_id(user_id, db)
    logger.info(f"[ROUTER] Found user: {user} with ID {user_id}.")
    return user


@router.get('/users/{user_id}', response_model=UserEmployeesResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_users_by_user_id(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching users for user ID {user_id}.")
    users_user = user_repository.get_users_by_user_id(user_id, db)
    logger.info(f"[ROUTER] Found {len(users_user)} users for user ID {user_id}.")
    return users_user


@router.get('/warehouses/{user_id}', response_model=UserWarehousesResponseSchema, status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                 "Not authenticated or invalid role provided"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                              "User with ID {user_id} does not exist"),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error")})
def get_warehouses_by_user_id(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching warehouses for user ID {user_id}.")
    warehouses_user = user_repository.get_warehouses_by_user_id(user_id, db)
    logger.info(f"[ROUTER] Found {len(warehouses_user)} warehouses for user ID {user_id}.")
    return warehouses_user


@router.get('/alerts/{user_id}', response_model=UserAlertsResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_alerts_by_user_id(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching alerts for user ID {user_id}.")
    alerts_user = user_repository.get_alerts_by_user_id(user_id, db)
    logger.info(f"[ROUTER] Found {len(alerts_user)} alerts for user ID {user_id}.")
    return alerts_user


@router.post('/', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create user error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    logger.info("[ROUTER] Creating new user.")
    created_user = user_repository.create_user(user, db)
    logger.info(f"[ROUTER] User created: {created_user}")
    return created_user


@router.put('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Update user error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def update_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Updating user with ID {user_id}.")
    edited_user = user_repository.update_user(user_id, user, db)
    logger.info(f"[ROUTER] User with ID {user_id} updated: {edited_user}.")
    return edited_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Deleting user with ID {user_id}.")
    user_repository.delete_user(user_id, db)
    logger.info(f"[ROUTER] User with ID {user_id} deleted.")
    return None
