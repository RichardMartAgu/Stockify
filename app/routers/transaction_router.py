from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils.logger import logger
from app.repository import transaction_repository
from app.schemas.token_schema import TokenData
from app.schemas.transaction_schema import CreateTransactionSchema, TransactionResponseSchema, \
    TransactionProductsResponseSchema
from app.utils.error_response import get_error_response
from app.utils.oauth import role_required

router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"]
)


@router.get('/', response_model=List[TransactionResponseSchema], status_code=status.HTTP_200_OK,
            description="This endpoint is available to Admin transactions.",
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error"), })
def get_transactions(db: Session = Depends(get_db),
                     current_transaction: TokenData = Depends(role_required(['Admin']))):
    transaction_data = transaction_repository.get_transactions(db)
    return transaction_data


@router.post('/', response_model=TransactionProductsResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create transaction error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_transaction(transaction: CreateTransactionSchema, db: Session = Depends(get_db)):
    logger.info("[ROUTER] Fetching all transactions.")
    created_transaction = transaction_repository.create_transaction(transaction, db)
    logger.info(f"[ROUTER] Fetched {len(created_transaction)} transactions.")
    return created_transaction


@router.get('/{transaction_id}', response_model=TransactionResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                  "Transaction with ID {transaction_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching transactions with ID {transaction_id}.")
    transaction = transaction_repository.get_transaction_by_id(transaction_id, db)
    logger.info(f"[ROUTER] Found transactions: {transaction} with ID {transaction_id}.")
    return transaction


@router.get('/products/{transaction_id}', response_model=TransactionProductsResponseSchema,
            status_code=status.HTTP_200_OK, responses={
        status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                         "Not authenticated or invalid role provided"),
        status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
        status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                      "Transaction with ID {transaction_id} does not exist"),
        status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                  "Internal Server Error")})
def get_products_by_transaction_id(transaction_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Fetching products for transaction ID {transaction_id}.")
    products_transaction = transaction_repository.get_products_by_transaction_id(transaction_id, db)
    logger.info(f"[ROUTER] Found {len(products_transaction)} transactions for transaction ID {transaction_id}.")
    return products_transaction


@router.delete('/{transaction_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                  "Transaction with ID {transaction_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    logger.info(f"[ROUTER] Deleting transaction with ID {transaction_id}.")
    transaction_repository.delete_transaction(transaction_id, db)
    logger.info(f"[ROUTER] Transaction with ID {transaction_id} deleted.")
    return None
