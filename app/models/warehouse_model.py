from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    address = Column(String(255))
    phone = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # Relations
    warehouse_user = relationship("User", back_populates="user_warehouses")

    warehouse_products = relationship("Product", back_populates="product_warehouse")

    warehouse_transactions = relationship("Transaction", back_populates="transaction_warehouse")