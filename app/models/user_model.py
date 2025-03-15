from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = 'user'

    default_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    image_url = Column(String, nullable=True, server_default=default_image_url)

    admin_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)

    employees = relationship("User", backref="admin", remote_side=[id], cascade="all, delete-orphan",
                             single_parent=True, passive_deletes=True)
