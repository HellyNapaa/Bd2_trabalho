# controller/controller.py

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
        from view.view import OrderView  # Importando aqui para evitar ciclo de importação

        order_data, order_details_data = OrderView.get_order_input()

        order = Order(
            order_id=order_data['orderid'],
            customer_id=order_data['customerid'],
            employee_id=order_data['employeeid'],
            order_date=order_data['orderdate'],
            required_date=order_data['requireddate'],
            shipped_date=order_data['shippeddate'],
            freight=order_data['freight'],
            ship_name=order_data['ship_name'],
            ship_address=order_data['shipaddress'],
            ship_city=order_data['shipcity'],
            ship_region=order_data['shipregion'],
            ship_postal_code=order_data['shippostalcode'],
            ship_country=order_data['shipcountry'],
            shipper_id=order_data['shipperid']
        )

        order_details = [
            OrderDetail(
                order_id=order_data['orderid'],
                product_id=detail['product_id'],
                unit_price=detail['unitprice'],
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
