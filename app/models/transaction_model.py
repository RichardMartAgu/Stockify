from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.transaction_products_midtable import transaction_products


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    type = Column(String(50), index=True, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id", ondelete="CASCADE"), nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

    # Relations
    products = relationship('Product', secondary=transaction_products, back_populates='transactions')
    transaction_warehouse = relationship("Warehouse", back_populates="warehouse_transaction")
    transaction_clients = relationship("Client", back_populates="client_transactions")


    # Constraints
    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
    )
