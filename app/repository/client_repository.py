from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.client_model import Client
from app.models.transaction_model import Transaction


def get_clients(db: Session):
    data = db.query(Client).all()
    return data


def get_client_by_id(client_id: int, db: Session):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )
    return client

def get_transactions_by_client_id(client_id: int, db: Session):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )

    transactions = db.query(Transaction).filter(Transaction.client_id == client.id).all()

    if not transactions:
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

    return client_data


def create_client(client, db: Session):
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
            return new_client
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error create client: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Create client error {e}"
        )


def delete_client(client_id: int, db: Session):
    client_exists = db.query(Client).filter(Client.id == client_id).first()
    if not client_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )
    try:
        db.query(Client).filter(Client.id == client_id).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting client: {str(e)}"
        )
    return None


def update_client(client_id: int, client_update, db: Session):
    client = db.query(Client).filter(Client.id == client_id)
    client_instance = client.first()

    if not client_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with ID {client_id} does not exist"
        )

    try:
        client.update(client_update.dict(exclude_unset=True))
        db.commit()
        db.refresh(client_instance)  # Refresca los datos después del commit
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating client: {str(e)}"
        )

    return client_instance
