from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = 'user'

    # Default URL for the user image
    default_image_url = "https://res.cloudinary.com/dddghjiwv/image/upload/v1744883802/x5ut8o8tn79nrxo5zsky.jpg"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    password = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(50), nullable=False)
    stripe_customer_id = Column(String(150), unique=True, nullable=True)
    stripe_subscription_status = Column(Boolean, default=False, nullable=False)
    image_url = Column(String(500), nullable=True, server_default=default_image_url)
    admin_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    # Relationship
    users = relationship("User", backref="admin", remote_side=[id], lazy="joined")
    user_warehouses = relationship("Warehouse", back_populates="warehouse_user")
    user_clients = relationship("Client", back_populates="client_user")
    user_alerts = relationship("Alert", back_populates="alert_user")
