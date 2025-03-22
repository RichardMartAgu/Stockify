from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.transaction_products_midtable import transaction_products


class Product(Base):
    __tablename__ = 'product'

    # Default URL for the product image
    default_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    quantity = Column(Integer, index=True, nullable=False)
    serial_number = Column(String(30), index=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(String(255))
    kit_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=True)
    category = Column(String(50), index=True)
    image_url = Column(String(255), nullable=True, default=default_image_url)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id", ondelete="CASCADE"), nullable=False)

    # Relationship
    product_kit = relationship("Product", backref="kit_products", remote_side=[id])
    product_warehouse = relationship("Warehouse", back_populates="warehouse_products")
    transactions = relationship('Transaction', secondary=transaction_products, back_populates='products')
    product_alerts = relationship("Alert", back_populates="alert_product")

    # Constraints
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),

        # Ensures that a serial number is not repeated within the same warehouse
        UniqueConstraint('serial_number', 'warehouse_id', name='uq_serial_warehouse')

    )
