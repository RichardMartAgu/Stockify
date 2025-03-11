from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)

    admin_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)

    employees = relationship("User", backref="admin", remote_side=[id], cascade="all, delete-orphan",
                             single_parent=True, passive_deletes=True )
