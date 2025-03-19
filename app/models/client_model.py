from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(100), index=True, nullable=False, unique=True)
    name = Column(String(150), index=True, nullable=False)
    contact = Column(String(150))
    phone = Column(String(50))
    email = Column(String(150))
    address = Column(String(200))

    # Relations
    client_transactions = relationship("Transaction", back_populates="transaction_client")
