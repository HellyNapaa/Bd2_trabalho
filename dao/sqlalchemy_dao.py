from config.config import SessionLocal
from model.models import Order, OrderDetail, Employee, Customer
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
    def get_order_details(order_id):
        session = SessionLocal()
        try:
            order = session.query(Order).filter(Order.orderid == order_id).first()
            if order:
                details = session.query(OrderDetail).filter(OrderDetail.orderid == order_id).all()
                customer = session.query(Customer).filter(Customer.customerid == order.customerid).first()
                employee = session.query(Employee).filter(Employee.employeeid == order.employeeid).first()

                return order, details, employee, customer
            return None, None, None, None
        finally:
            session.close()

    @staticmethod
    def get_employee_ranking(start_date, end_date):
        session = SessionLocal()
        try:
            ranking = session.query(
                (Employee.firstname + ' ' + Employee.lastname).label('employeename'),
                func.count(Order.orderid).label('totalorders'),
                func.sum(OrderDetail.unitprice * OrderDetail.quantity).label('totalsales')
            ).join(Order, Employee.employeeid == Order.employeeid
            ).join(OrderDetail, Order.orderid == OrderDetail.orderid
            ).filter(
                Order.orderdate.between(start_date, end_date)
            ).group_by(
                Employee.employeeid
            ).order_by(
                desc(func.sum(OrderDetail.unitprice * OrderDetail.quantity))
            ).all()
            return ranking
        finally:
            session.close()
