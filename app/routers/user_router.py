from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repository import user_repository
from app.schemas.token_schema import TokenData
from app.schemas.user_schema import UpdateUserSchema, CreateUserSchema, UserResponseSchema, UserEmployeesResponseSchema, \
    UserWarehousesResponseSchema, UserAlertsResponseSchema, UserClientsResponseSchema
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
    users_data = user_repository.get_users(db)
    return users_data


@router.get('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_repository.get_user_by_id(user_id, db)
    return user


@router.get('/users/{user_id}', response_model=UserEmployeesResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_users_by_user_id(user_id: int, db: Session = Depends(get_db)):
    users_user = user_repository.get_users_by_user_id(user_id, db)
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
    warehouses_user = user_repository.get_warehouses_by_user_id(user_id, db)
    return warehouses_user

@router.get('/clients/{user_id}', response_model=UserClientsResponseSchema, status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                 "Not authenticated or invalid role provided"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                              "User with ID {user_id} does not exist"),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error")})
def get_clients_by_user_id(user_id: int, db: Session = Depends(get_db)):
    clients_user = user_repository.get_clients_by_user_id(user_id, db)
    return clients_user


@router.get('/alerts/{user_id}', response_model=UserAlertsResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_alerts_by_user_id(user_id: int, db: Session = Depends(get_db)):
    alerts_user = user_repository.get_alerts_by_user_id(user_id, db)
    return alerts_user


@router.post('/', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create user error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    created_user = user_repository.create_user(user, db)
    return created_user


@router.put('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Update user error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def update_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(get_db)):
    edited_user = user_repository.update_user(user_id, user, db)
    return edited_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "User with ID {user_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repository.delete_user(user_id, db)
    return None
