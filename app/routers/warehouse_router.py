from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repository import warehouse_repository
from app.schemas.token_schema import TokenData
from app.schemas.warehouse_schema import UpdateWarehouseSchema, CreateWarehouseSchema, WarehouseResponseSchema, \
    WarehouseProductsResponseSchema, WarehouseTransactionsResponseSchema
from app.utils.error_response import get_error_response
from app.utils.oauth import role_required

router = APIRouter(
    prefix="/warehouse",
    tags=["Warehouse"]
)


@router.get('/', response_model=List[WarehouseResponseSchema], status_code=status.HTTP_200_OK,
            description="This endpoint is available to Admin user.",
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error"), })
def get_warehouses(db: Session = Depends(get_db),
              current_warehouse: TokenData = Depends(role_required(['Admin']))):
    data = warehouse_repository.get_warehouses(db)
    return data


@router.post('/', response_model=WarehouseResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create warehouse error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_warehouse(warehouse: CreateWarehouseSchema, db: Session = Depends(get_db)):
    created_warehouse = warehouse_repository.create_warehouse(warehouse, db)
    return created_warehouse


@router.get('/{warehouse_id}', response_model=WarehouseResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_warehouse_by_id(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = warehouse_repository.get_warehouse_by_id(warehouse_id, db)
    return warehouse

@router.get('/products/{warehouse_id}', response_model=WarehouseProductsResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_products_by_product_id(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = warehouse_repository.get_products_by_warehouse_id(warehouse_id, db)
    return warehouse

@router.get('/transactions/{warehouse_id}', response_model=WarehouseTransactionsResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_transactions_by_product_id(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse = warehouse_repository.get_transactions_by_warehouse_id(warehouse_id, db)
    return warehouse


@router.delete('/{warehouse_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse_repository.delete_warehouse(warehouse_id, db)
    return None


@router.put('/{warehouse_id}', response_model=WarehouseResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Update warehouse error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def update_warehouse(warehouse_id: int, warehouse: UpdateWarehouseSchema, db: Session = Depends(get_db)):
    edited_warehouse = warehouse_repository.update_warehouse(warehouse_id, warehouse, db)
    return edited_warehouse
