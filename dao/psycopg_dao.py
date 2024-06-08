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
                    SELECT o.orderid, o.orderdate, o.requireddate, o.shippeddate, o.freight,
                        o.shipname, o.shipaddress, o.shipcity, o.shipregion, o.shippostalcode, o.shipcountry,
                        o.shipperid, od.productid, od.unitprice, od.quantity, od.discount
                    FROM northwind.orders o
                    JOIN northwind.order_details od ON o.orderid = od.orderid
                    WHERE o.orderid = %s
                """, (order_id,))
                result = cur.fetchall()
            
                if result:
                    order_data = result[0]
                    order = Order(
                        orderid=order_data[0],         
                        orderdate=order_data[1],       
                        requireddate=order_data[2],    
                        shippeddate=order_data[3],     
                        freight=order_data[4],         
                        shipname=order_data[5],        
                        shipaddress=order_data[6],     
                        shipcity=order_data[7],        
                        shipregion=order_data[8],      
                        shippostalcode=order_data[9], 
                        shipcountry=order_data[10],     
                        shipperid=order_data[11]        
                    )

                    details = [
                        OrderDetail(
                            productid=row[12],  
                            unitprice=row[13],  
                            quantity=row[14],   
                            discount=row[15]   
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
