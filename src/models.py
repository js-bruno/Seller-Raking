"""
Defining columns for database
persistence using sqlalchemy.

With a basic many to one relationship between Sale and Seller.
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Sale(Base):  # pylint: disable=too-few-public-methods
    """
    Column to persist sales data
    """

    __tablename__ = "sale"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("seller.id"))
    customer_name = Column(String(500))
    date_sale = Column(String(50))
    item_name = Column(String(500))
    item_value = Column(Float)


class Seller(Base):  # pylint: disable=too-few-public-methods
    """
    Column to Seller data
    """

    __tablename__ = "seller"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500))
    sales = relationship("Sale", backref="seller")
