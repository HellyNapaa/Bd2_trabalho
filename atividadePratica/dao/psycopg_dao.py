# dao/psycopg_dao.py

from config.config import get_psycopg_connection
from model.models import Order, OrderDetail

class OrderDAOPsycopg:
    @staticmethod
    def insert_order(order, order_details):
        conn = get_psycopg_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO northwind.orders (
                        orderid, customerid, employeeid, orderdate, 
                        requireddate, shippeddate, freight, shipname, 
                        shipaddress, shipcity, shipregion, shippostalcode, 
                        shipcountry, shipperid
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING orderid
                    """,
                    (
                        order.order_id, order.customer_id, order.employee_id, order.order_date,
                        order.required_date, order.shipped_date, order.freight, order.ship_name,
                        order.ship_address, order.ship_city, order.ship_region, order.ship_postal_code,
                        order.ship_country, order.shipper_id
                    )
                )
                order_id = cur.fetchone()[0]
                for detail in order_details:
                    cur.execute(
                        """
                        INSERT INTO northwind.order_details (
                            orderid, productid, unitprice, quantity, discount
                        ) VALUES (
                            %s, %s, %s, %s, %s
                        )
                        """,
                        (
                            order_id, detail.product_id, detail.unit_price, detail.quantity, detail.discount
                        )
                    )
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_order_details(orderid):
        conn = get_psycopg_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT o.orderid, o.orderdate, o.requireddate, o.shippeddate, o.freight,
                           o.shipname, o.shipaddress, o.shipcity, o.shipregion, o.shippostalcode, o.shipcountry,
                           o.shipperid, od.productid, od.unitprice, od.quantity, od.discount
                    FROM northwind.orders o
                    JOIN northwind.order_details od ON o.orderid = od.orderid
                    WHERE o.orderid = %s
                """, (orderid,))
                result = cur.fetchall()

                if result:
                    order_data = result[0]
                    order = Order(
                        orderid=order_data[0],  # orderid
                        orderdate=order_data[1],  # orderdate
                        requireddate=order_data[2],  # requireddate
                        shippe_date=order_data[3],  # shippeddate
                        freight=order_data[4],  # freight
                        shipname=order_data[5],  # shipname
                        shipaddress=order_data[6],  # shipaddress
                        shipcity=order_data[7],  # shipcity
                        shipregion=order_data[8],  # shipregion
                        shippostal_code=order_data[9],  # shippostalcode
                        shipcountry=order_data[10],  # shipcountry
                        shipper_id=order_data[11]  # shipperid
                    )

                    details = [
                        OrderDetail(
                            product_id=row[12],  # productid
                            unit_price=row[13],  # unitprice
                            quantity=row[14],  # quantity
                            discount=row[15]  # discount
                        ) for row in result
                    ]

                    return order, details
                else:
                    return None, None
        finally:
            conn.close()

    @staticmethod
    def get_employee_ranking(start_date, end_date):
        conn = get_psycopg_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.firstname || ' ' || e.lastname AS employeename, COUNT(o.orderid) AS totalorders, SUM(od.unitprice * od.quantity) AS totalsales
                    FROM northwind.employees e
                    JOIN northwind.orders o ON e.employeeid = o.employeeid
                    JOIN northwind.order_details od ON o.orderid = od.orderid
                    WHERE o.orderdate BETWEEN %s AND %s
                    GROUP BY e.employeeid
                    ORDER BY totalsales DESC
                """, (start_date, end_date))
                result = cur.fetchall()
                return result
        finally:
            conn.close()
