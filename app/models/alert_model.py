from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Alert(Base):
    __tablename__ = 'alert'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False, server_default=func.now())
    read = Column(Boolean, nullable=False, default=False)
    min_quantity = Column(Integer)
    max_quantity = Column(Integer)
    max_message = Column(String(500))
    min_message = Column(String(500))
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # Relations
    alert_product = relationship("Product", back_populates="product_alerts")
    alert_user = relationship("User", back_populates="user_alerts")

    # Constraints
    __table_args__ = (
        CheckConstraint('max_quantity >= 0', name='check_max_quantity_non_negative'),
        CheckConstraint('min_quantity >= 0', name='check_min_quantity_non_negative'),
        CheckConstraint(
            "(min_quantity IS NOT NULL AND max_quantity IS NULL) OR "
            "(min_quantity IS NULL AND max_quantity IS NOT NULL)",
            name="check_discount_or_offer"
        ),
    )

