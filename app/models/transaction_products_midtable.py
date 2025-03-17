from sqlalchemy import Column, Integer, ForeignKey, Table, CheckConstraint

from app.db.database import Base

transaction_products = Table(
    'transaction_products', Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transaction.id', ondelete='CASCADE'), primary_key=True),
          Column('product_id', Integer, ForeignKey('product.id', ondelete='CASCADE'), primary_key=True),
          Column('quantity', Integer, nullable=False)
)

__table_args__ = (
        CheckConstraint('quantity >= 0', name='check_price_non_negative'),
)