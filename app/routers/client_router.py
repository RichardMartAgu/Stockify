from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repository import client_repository
from app.schemas.client_schema import UpdateClientSchema, CreateClientSchema, ClientResponseSchema, \
    ClientTransactionsResponseSchema
from app.schemas.token_schema import TokenData
from app.utils.error_response import get_error_response
from app.utils.logger import logger
from app.utils.oauth import role_required

router = APIRouter(
    prefix="/client",
    tags=["Client"]
)


@router.get('/', response_model=List[ClientResponseSchema], status_code=status.HTTP_200_OK,
            description="This endpoint is available to Admin clients.",
            responses={
                status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                                 "Not authenticated or invalid role provided"),
                status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN",
                                                              "You do not have access to this resource."),
                status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                          "Internal Server Error"), })
def get_clients(db: Session = Depends(get_db),
                current_client: TokenData = Depends(role_required(['Admin']))):
    logger.info("[ROUTER] Fetching all clients.")
    client_data = client_repository.get_clients(db)
    logger.info(f"[ROUTER] Fetched {len(client_data)} clients.")
    return client_data


@router.get('/{client_id}', response_model=ClientResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                     "Not authenticated or invalid role provided"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Client with ID {client_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def get_client_by_id(client_id: int, db: Session = Depends(get_db),
                     current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Fetching client with ID {client_id}.")
    client = client_repository.get_client_by_id(client_id, db)
    logger.info(f"[ROUTER] Found client: {client} with ID {client_id}.")
    return client


@router.get('/transactions/{client_id}', response_model=ClientTransactionsResponseSchema,
            status_code=status.HTTP_200_OK, responses={
        status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED",
                                                         "Not authenticated or invalid role provided"),
        status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
        status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Client with ID {client_id} does not exist"),
        status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR",
                                                                  "Internal Server Error")})
def get_transactions_by_client_id(client_id: int, db: Session = Depends(get_db),
                                  current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Fetching transactions for client ID {client_id}.")
    transactions_client = client_repository.get_transactions_by_client_id(client_id, db)
    logger.info(f"[ROUTER] Found {len(transactions_client)} transactions for client ID {client_id}.")
    return transactions_client


@router.post('/', response_model=ClientResponseSchema, status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Create client error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def create_client(client: CreateClientSchema, db: Session = Depends(get_db),
                  current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info("[ROUTER] Creating new client.")
    created_client = client_repository.create_client(client, db)
    logger.info(f"[ROUTER] Client created: {created_client}")
    return created_client


@router.put('/{client_id}', response_model=ClientResponseSchema, status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Client with ID {client_id} does not exist"),
    status.HTTP_409_CONFLICT: get_error_response("ERROR: CONFLICT", "Update client error {e}"),
    status.HTTP_422_UNPROCESSABLE_ENTITY: get_error_response("ERROR: UNPROCESSABLE ENTITY", "Expecting value"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def update_client(client_id: int, client: UpdateClientSchema, db: Session = Depends(get_db),
                  current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Updating client with ID {client_id}.")
    edited_client = client_repository.update_client(client_id, client, db)
    logger.info(f"[ROUTER] Client with ID {client_id} updated: {edited_client}.")
    return edited_client


@router.delete('/{client_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_204_NO_CONTENT: {"description": "NO_CONTENT"},
    status.HTTP_401_UNAUTHORIZED: get_error_response("ERROR: UNAUTHORIZED", "Not authenticated"),
    status.HTTP_403_FORBIDDEN: get_error_response("ERROR: FORBIDDEN", "You do not have access to this resource."),
    status.HTTP_404_NOT_FOUND: get_error_response("ERROR: NOT FOUND", "Client with ID {client_id} does not exist"),
    status.HTTP_500_INTERNAL_SERVER_ERROR: get_error_response("ERROR: INTERNAL SERVER ERROR", "Internal Server Error")})
def delete_client(client_id: int, db: Session = Depends(get_db),
                  current_user: TokenData = Depends(role_required(['Admin']))):
    logger.info(f"[ROUTER] Deleting client with ID {client_id}.")
    client_repository.delete_client(client_id, db)
    logger.info(f"[ROUTER] Client with ID {client_id} deleted.")
    return None
