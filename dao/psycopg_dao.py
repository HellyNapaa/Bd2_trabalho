from config.config import get_psycopg_connection
from model.models import Order, OrderDetail, Employee, Customer

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
                        order.orderid, order.customerid, order.employeeid, order.orderdate,
                        order.requireddate, order.shippeddate, order.freight, order.shipname,
                        order.shipaddress, order.shipcity, order.shipregion, order.shippostalcode,
                        order.shipcountry, order.shipperid
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
                            order_id, detail.productid, detail.unitprice, detail.quantity, detail.discount
                        )
                    )
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_order_details(order_id):
        conn = get_psycopg_connection()
        print("conexão okay")
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT o.orderid, c.contactname, e.firstname, o.orderdate,
                        od.productid, od.unitprice, od.quantity
                    FROM northwind.orders o
                    JOIN northwind.order_details od ON o.orderid = od.orderid
                    JOIN northwind.customers c ON o.customerid = c.customerid
                    JOIN northwind.employees e ON o.employeeid = e.employeeid
                    WHERE o.orderid = %s
                """, (order_id,))
                result = cur.fetchall()
            
                if result:
                    order_data = result[0]
                    order = Order(
                        orderid=order_data[0],
                        orderdate=order_data[3]
                    )
                    customer = Customer(
                        contactname=order_data[1]
                    )
                    employee = Employee(
                        firstname=order_data[2]
                    )
                    details = [
                        OrderDetail(
                            productid=row[4],
                            unitprice=row[5],
                            quantity=row[6]
                        ) for row in result
                    ]

                    return order, details, employee, customer
                else:
                    return None, None, None, None
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
