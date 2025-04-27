from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class TransactionProduct(Base):
    __tablename__ = "transaction_products"

    transaction_id = Column(Integer, ForeignKey("transaction.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    # Relaciones ORM
    transaction = relationship("Transaction", back_populates="transaction_products")
    product = relationship("Product", back_populates="transaction_products")
