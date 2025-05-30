from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = 'user'

    # Default URL for the user image
    default_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"

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
