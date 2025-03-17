from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class Alert(Base):
    __tablename__ = 'alert'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    max_quantity = Column(Integer)
    min_quantity = Column(Integer, nullable=False)
    max_message = Column(String(500))
    min_message = Column(String(500))
    Read = Column(Boolean, nullable=False, default= False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    # Relations
    alert_product = relationship("Product", back_populates="product_alerts")
    alert_user = relationship("User", back_populates="user_alerts")

    # Constraints
    __table_args__ = (
        CheckConstraint('max_quantity >= 0', name='check_max_quantity_non_negative'),
        CheckConstraint('min_quantity >= 0', name='check_min_quantity_non_negative'),
    )
