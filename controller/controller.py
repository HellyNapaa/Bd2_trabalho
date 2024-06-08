from dao.psycopg_dao import OrderDAOPsycopg
from dao.sqlalchemy_dao import OrderDAOSQLAlchemy
from model.models import Order, OrderDetail

class OrderController:
    def __init__(self, dao_type):
        if dao_type == 'psycopg':
            self.dao = OrderDAOPsycopg()
        elif dao_type == 'sqlalchemy':
            self.dao = OrderDAOSQLAlchemy()
        else:
            raise ValueError("Invalid DAO type")

    def create_order(self):
        from view.view import OrderView 

        order_data, order_details_data = OrderView.get_order_input()

        order = Order(
            orderid=order_data['orderid'],
            customerid=order_data['customerid'],
            employeeid=order_data['employeeid'],
            orderdate=order_data['orderdate'],
            requireddate=order_data['requireddate'],
            shippeddate=order_data['shippeddate'],
            freight=order_data['freight'],
            shipname=order_data['shipname'],
            shipaddress=order_data['shipaddress'],
            shipcity=order_data['shipcity'],
            shipregion=order_data['shipregion'],
            shippostalcode=order_data['shippostalcode'],
            shipcountry=order_data['shipcountry'],
            shipperid=order_data['shipperid']
        )

        order_details = [
            OrderDetail(
                orderid=order_data['orderid'],
                productid=detail['productid'],
                unitprice=detail['unitprice'],
                quantity=detail['quantity'],
                discount=detail['discount']
            ) for detail in order_details_data
        ]

        self.dao.insert_order(order, order_details)
        print("Order created successfully!")

    def show_order_details(self, order_id):
        order, details = self.dao.get_order_details(order_id)
        from view.view import OrderView
        OrderView.display_order_details(order, details)

    def show_employee_ranking(self, start_date, end_date):
        ranking = self.dao.get_employee_ranking(start_date, end_date)
        from view.view import OrderView
        OrderView.display_employee_ranking(ranking)