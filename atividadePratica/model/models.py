# model/models.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    __table_args__ = {'schema': 'northwind'}
    customer_id = Column(String, primary_key=True)
    company_name = Column(String)
    orders = relationship('Order', back_populates='customer')

class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'northwind'}
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    orders = relationship('Order', back_populates='employee')

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'northwind'}
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    order_date = Column(Date)
    required_date = Column(Date)
    shipped_date = Column(Date)
    freight = Column(Numeric(15, 4))  # Numeric(precision, scale)
    ship_name = Column(String(35))
    ship_address = Column(String(50))
    ship_city = Column(String(15))
    ship_region = Column(String(15))
    ship_postal_code = Column(String(9))
    ship_country = Column(String(15))
    shipper_id = Column(Integer)

    customer = relationship('Customer', back_populates='orders')
    employee = relationship('Employee', back_populates='orders')
    order_details = relationship('OrderDetail', back_populates='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'
    __table_args__ = {'schema': 'northwind'}
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    product_id = Column(Integer, primary_key=True)
    unit_price = Column(Numeric(15, 4))  # Numeric(precision, scale)
    quantity = Column(Integer)
    discount = Column(Numeric(15, 4))  # Numeric(precision, scale)

    order = relationship('Order', back_populates='order_details')

# Back-populate relationships
Order.customer = relationship('Customer', back_populates='orders')
Order.employee = relationship('Employee', back_populates='orders')
OrderDetail.order = relationship('Order', back_populates='order_details')
