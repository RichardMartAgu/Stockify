from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(255), index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    contact = Column(String(255))
    phone = Column(String(50))
    email = Column(String(255))
    address = Column(String(255))

    # Relations
    client_transactions = relationship("Transaction", back_populates="transaction_client")
