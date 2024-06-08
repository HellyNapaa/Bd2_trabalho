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
                detail.order_id = order.orderid
                session.add(detail)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def get_order_details(orderid):
        session = SessionLocal()
        try:
            order = session.query(Order).filter(Order.orderid == orderid).first()
            if order:
                details = session.query(OrderDetail).filter(OrderDetail.orderid == orderid).all()
                return order, details
            return None, None
        finally:
            session.close()

    @staticmethod
    def get_employee_ranking(start_date, end_date):
        session = SessionLocal()
        try:
            ranking = session.query(
                Employee.firstname + ' ' + Employee.lastname,
                func.count(Order.orderid).label('totalorders'),
                func.sum(OrderDetail.unitprice * OrderDetail.quantity).label('totalsales')
            ).join(Order).join(OrderDetail).filter(
                Order.orderdate.between(start_date, end_date)
            ).group_by(
                Employee.employeeid
            ).order_by(
                desc(func.sum(OrderDetail.unitprice * OrderDetail.quantity))
            ).all()
            return ranking
        finally:
            session.close()
