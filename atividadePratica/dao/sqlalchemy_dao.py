# dao/sqlalchemy_dao.py

from config.config import SessionLocal
from model.models import Order, OrderDetail, Employee
from sqlalchemy import func, desc

class OrderDAOSQLAlchemy:
    @staticmethod
    def insert_order(order, order_details):
        session = SessionLocal()
        try:
            session.add(order)
            session.commit()
            session.refresh(order)
            for detail in order_details:
                detail.order_id = order.order_id
                session.add(detail)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def get_order_details(order_id):
        session = SessionLocal()
        try:
            order = session.query(Order).filter(Order.order_id == order_id).first()
            if order:
                details = session.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()
                return order, details
            return None, None
        finally:
            session.close()

    @staticmethod
    def get_employee_ranking(start_date, end_date):
        session = SessionLocal()
        try:
            ranking = session.query(
                Employee.first_name,
                Employee.last_name,
                func.count(Order.order_id).label('total_orders'),
                func.sum(OrderDetail.unit_price * OrderDetail.quantity).label('total_sales')
            ).join(Order).join(OrderDetail).filter(
                Order.order_date.between(start_date, end_date)
            ).group_by(
                Employee.employee_id
            ).order_by(
                desc('total_sales')
            ).all()
            return ranking
        finally:
            session.close()
