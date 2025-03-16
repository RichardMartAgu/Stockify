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
    owner = relationship("User", back_populates="owned_warehouses")

    warehouse_products = relationship("Product", back_populates="product_warehouses", cascade="all, delete-orphan",
                                       single_parent=True,
                                       passive_deletes=True)
