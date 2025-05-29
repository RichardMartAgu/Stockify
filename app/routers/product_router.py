from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repository import product_repository
from app.schemas.product_schema import UpdateProductSchema, CreateProductSchema, ProductResponseSchema, \
    ProductProductsResponseSchema, ProductTransactionsResponseSchema, ProductAlertsResponseSchema
from app.schemas.token_schema import TokenData
from app.utils.error_response import get_error_response
from app.utils.logger import logger
from app.utils.oauth import role_required

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)


@router.get('/', response_model=List[ProductResponseSchema], status_code=status.HTTP_200_OK,
            description="This endpoint is available to Admin products.",
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                 "Not authenticated or invalid role provided"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error"), })
def get_products(db: Session = Depends(get_db),
                 current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info("[ROUTER] Fetching all products.")
    product_data = product_repository.get_products(db)
    logger.info(f"[ROUTER] Fetched {len(product_data)} products.")
    return product_data


@router.get('/{product_id}', response_model=ProductResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Product with ID {product_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_product_by_id(product_id: int, db: Session = Depends(get_db),
                      current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Fetching product with ID {product_id}.")
    product = product_repository.get_product_by_id(product_id, db)
    logger.info(f"[ROUTER] Found product: {product} with ID {product_id}.")
    return product


@router.get('/products/{product_id}', response_model=ProductProductsResponseSchema, status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                 "Not authenticated or invalid role provided"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                              "Product with ID {product_id} does not exist"),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error")})
def get_products_by_product_id(product_id: int, db: Session = Depends(get_db),
                               current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Fetching products for client ID {product_id}.")
    products_product = product_repository.get_products_by_product_id(product_id, db)
    logger.info(f"[ROUTER] Found {len(products_product)} products for client ID {product_id}.")
    return products_product


@router.get('/transactions/{product_id}', response_model=ProductTransactionsResponseSchema,
            status_code=status.HTTP_200_OK, responses={
        status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                         "Not authenticated or invalid role provided"),
        status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
        status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                      "Product with ID {product_id} does not exist"),
        status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                  "Internal Server Error")})
def get_transactions_by_product_id(product_id: int, db: Session = Depends(get_db),
                                   current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Fetching transactions for product ID {product_id}.")
    transactions_product = product_repository.get_transactions_by_product_id(product_id, db)
    logger.info(f"[ROUTER] Found {len(transactions_product)} transactions for product ID {product_id}.")
    return transactions_product


@router.get('/alerts/{product_id}', response_model=ProductAlertsResponseSchema, status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                 "Not authenticated or invalid role provided"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                              "Product with ID {product_id} does not exist"),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error")})
def get_alerts_by_product_id(product_id: int, db: Session = Depends(get_db),
                             current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Fetching alerts for product ID {product_id}.")
    alerts_product = product_repository.get_alerts_by_product_id(product_id, db)
    logger.info(f"[ROUTER] Found {len(alerts_product)} alerts for product ID {product_id}.")
    return alerts_product


@router.post('/', response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create product error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_product(product: CreateProductSchema, db: Session = Depends(get_db),
                   current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info("[ROUTER] Creating new product.")
    created_product = product_repository.create_product(product, db)
    logger.info(f"[ROUTER] Products created: {created_product}")
    return created_product


@router.put('/{product_id}', response_model=ProductResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Product with ID {product_id} does not exist"),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Update product error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def update_product(product_id: int, product: UpdateProductSchema, db: Session = Depends(get_db),
                   current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Updating product with ID {product_id}.")
    edited_product = product_repository.update_product(product_id, product, db)
    logger.info(f"[ROUTER] Product with ID {product_id} updated: {edited_product}.")
    return edited_product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Product with ID {product_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_product(product_id: int, db: Session = Depends(get_db),
                   current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Deleting product with ID {product_id}.")
    product_repository.delete_product(product_id, db)
    logger.info(f"[ROUTER] Product with ID {product_id} deleted.")
    return None
