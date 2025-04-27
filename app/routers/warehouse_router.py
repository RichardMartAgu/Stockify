from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils.logger import logger
from app.repository import warehouse_repository
from app.schemas.token_schema import TokenData
from app.schemas.warehouse_schema import UpdateWarehouseSchema, CreateWarehouseSchema, WarehouseResponseSchema, \
    WarehouseProductsResponseSchema, WarehouseTransactionsResponseSchema, warehouse_example
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
    logger.info("[ROUTER] Fetching all warehouses.")
    warehouse_data = warehouse_repository.get_warehouses(db)
    logger.info(f"[ROUTER] Fetched {len(warehouse_data)} warehouses.")
    return warehouse_data


@router.get('/{warehouse_id}', response_model=WarehouseResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                  "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_warehouse_by_id(warehouse_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching warehouse with ID {warehouse_id}.")
    warehouse = warehouse_repository.get_warehouse_by_id(warehouse_id, db)
    logger.info(f"[ROUTER] Found warehouse: {warehouse} with ID {warehouse_id}.")
    return warehouse


@router.get('/products/{warehouse_id}', response_model=WarehouseProductsResponseSchema, status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                 "Not authenticated or invalid role provided"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                              "Warehouse with ID {warehouse_id} does not exist"),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error")})
def get_products_by_warehouse_id(warehouse_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching products for warehouse ID {warehouse_id}.")
    products_warehouse = warehouse_repository.get_products_by_warehouse_id(warehouse_id, db)
    logger.info(f"[ROUTER] Found {len(products_warehouse)} products for client ID {warehouse_id}.")
    return products_warehouse


@router.get('/transactions/{warehouse_id}',
            status_code=status.HTTP_200_OK, responses={
        200: {
            "content": {
                "application/json": {
                    "example": warehouse_example
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                         "Not authenticated or invalid role provided"),
        status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
        status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                      "Warehouse with ID {warehouse_id} does not exist"),
        status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                  "Internal Server Error")
    })
def get_transactions_by_warehouse_id(warehouse_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching transactions for warehouse ID {warehouse_id}.")
    transactions_warehouse = warehouse_repository.get_transactions_by_warehouse_id(warehouse_id, db)
    logger.info(f"[ROUTER] Found {len(transactions_warehouse)} transactions for client ID {warehouse_id}.")
    return transactions_warehouse


@router.post('/', response_model=WarehouseResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create warehouse error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_warehouse(warehouse: CreateWarehouseSchema, db: Session = Depends(get_db)):
    logger.info("[ROUTER] Creating new warehouse.")
    created_warehouse = warehouse_repository.create_warehouse(warehouse, db)
    logger.info(f"[ROUTER] Warehouse created: {created_warehouse}")
    return created_warehouse


@router.put('/{warehouse_id}', response_model=WarehouseResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                  "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Update warehouse error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def update_warehouse(warehouse_id: int, warehouse: UpdateWarehouseSchema, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Updating warehouse with ID {warehouse_id}.")
    edited_warehouse = warehouse_repository.update_warehouse(warehouse_id, warehouse, db)
    logger.info(f"[ROUTER] Warehouse with ID {warehouse_id} updated: {edited_warehouse}.")
    return edited_warehouse


@router.delete('/{warehouse_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                  "Warehouse with ID {warehouse_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Deleting warehouse with ID {warehouse_id}.")
    warehouse_repository.delete_warehouse(warehouse_id, db)
    logger.info(f"[ROUTER] Warehouse with ID {warehouse_id} deleted.")
    return None
