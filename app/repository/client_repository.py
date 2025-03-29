from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils.logger import logger
from app.models.client_model import Client
from app.models.transaction_model import Transaction


def get_clients(db: Session):
    logger.info("Fetching all clients from the database.")
    data = db.query(Client).all()
    logger.info(f"Found {len(data)} clients.")
    return data


def get_client_by_id(client_id: int, db: Session):
    logger.info(f"Fetching client with ID {client_id}.")
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        logger.warning(f"Client with ID {client_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )
    logger.info(f"Client with ID {client_id} found.")
    return client


def get_transactions_by_client_id(client_id: int, db: Session):
    logger.info(f"Fetching transactions for client with ID {client_id}.")
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        logger.warning(f"Client with ID {client_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )

    transactions = db.query(Transaction).filter(Transaction.client_id == client.id).all()

    if not transactions:
        logger.warning(f"No transactions found for client with ID {client_id}.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No transactions found under client with ID {client_id}"
        )

    transactions_list = [
        {
            "id": transaction.id,
            "date": transaction.date,
            "type": transaction.type,
            "warehouse_id": transaction.warehouse_id,
            "client_id": transaction.client_id
        }
        for transaction in transactions
    ]

    client_data = {
        "id": client.id,
        "identifier": client.identifier,
        "name": client.name,
        "contact": client.contact,
        "phone": client.phone,
        "email": client.email,
        "address": client.address,
        "transactions": transactions_list
    }

    logger.info(f"Returning transactions for client with ID {client_id}.")
    return client_data


def create_client(client, db: Session):
    logger.info(f"Attempting to create a new client with identifier {client['identifier']}.")
    client = client.dict()
    try:
        contact = client.get("contact", None)
        phone = client.get("phone", None)
        email = client.get("email", None)
        address = client.get("address", None)

        new_client = Client(
            identifier=client["identifier"],
            name=client["name"],
            contact=contact,
            phone=phone,
            email=email,
            address=address
        )

        try:
            db.add(new_client)
            db.commit()
            db.refresh(new_client)
            logger.info(f"Client with identifier {new_client.identifier} created successfully.")
            return new_client
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating client: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating client: {str(e)}"
            )

    except Exception as e:
        db.rollback()
        logger.error(f"Error in client creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create client conflict {str(e)}"
        )


def update_client(client_id: int, client_update, db: Session):
    logger.info(f"Attempting to update client with ID {client_id}.")
    client = db.query(Client).filter(Client.id == client_id)
    client_instance = client.first()

    if not client_instance:
        logger.warning(f"Client with ID {client_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )

    try:
        client.update(client_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(client_instance)
        logger.info(f"Client with ID {client_id} updated successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating client: {str(e)}"
        )

    return client_instance


def delete_client(client_id: int, db: Session):
    logger.info(f"Attempting to delete client with ID {client_id}.")
    client_exists = db.query(Client).filter(Client.id == client_id).first()
    if not client_exists:
        logger.warning(f"Client with ID {client_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )

    try:
        db.query(Client).filter(Client.id == client_id).delete(synchronize_session=False)
        db.commit()
        logger.info(f"Client with ID {client_id} deleted successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting client: {str(e)}"
        )
    return None
