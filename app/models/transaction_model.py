from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(100), index=True, nullable=False, unique=True)
    date = Column(DateTime, index=True, nullable=False, server_default=func.now())
    type = Column(String(50), index=True, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id", ondelete="CASCADE"), nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=True)

    # Relationship
    transaction_products = relationship("TransactionProduct", back_populates="transaction", cascade="all, delete-orphan")
    transaction_warehouse = relationship("Warehouse", back_populates="warehouse_transactions")
    transaction_client = relationship("Client", back_populates="client_transactions")
