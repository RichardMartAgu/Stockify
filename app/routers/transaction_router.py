from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repository import transaction_repository
from app.schemas.token_schema import TokenData
from app.schemas.transaction_schema import CreateTransactionSchema, TransactionResponseSchema
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
    data = transaction_repository.get_transactions(db)
    return data


@router.post('/', response_model=TransactionResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create transaction error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_transaction(transaction: CreateTransactionSchema, db: Session = Depends(get_db)):
    created_transaction = transaction_repository.create_transaction(transaction, db)
    return created_transaction


@router.get('/{transaction_id}', response_model=TransactionResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                  "Transaction with ID {transaction_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    transaction = transaction_repository.get_transaction_by_id(transaction_id, db)
    return transaction


@router.delete('/{transaction_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},

    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND",
                                                  "Transaction with ID {transaction_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction_repository.delete_transaction(transaction_id, db)
    return None
