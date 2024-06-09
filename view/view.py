class OrderView:
    @staticmethod
    def get_order_input():
        orderid = input("Order ID: ")
        customerid = input("Customer ID: ")
        employeeid = input("Employee ID: ")
        orderdate = input("Order Date (YYYY-MM-DD): ")
        requireddate = input("Required Date (YYYY-MM-DD): ")
        shippeddate = input("Shipped Date (YYYY-MM-DD): ")
        freight = float(input("Freight: "))
        shipname = input("Ship Name: ")
        shipaddress = input("Ship Address: ")
        shipcity = input("Ship City: ")
        shipregion = input("Ship Region: ")
        shippostalcode = input("Ship Postal Code: ")
        shipcountry = input("Ship Country: ")
        shipperid = int(input("Shipper ID: "))
        
        order_data = {
            'orderid': orderid, 
            'customerid': customerid,
            'employeeid': employeeid,
            'orderdate': orderdate,
            'requireddate': requireddate,
            'shippeddate': shippeddate,
            'freight': freight,
            'shipname': shipname,
            'shipaddress': shipaddress,
            'shipcity': shipcity,
            'shipregion': shipregion,
            'shippostalcode': shippostalcode,
            'shipcountry': shipcountry,
            'shipperid': shipperid
        }

        order_details_data = []
        while True:
            productid = input("Product ID (or 'done' to finish): ")
            if productid.lower() == 'done':
                break
            unitprice = float(input("Unit Price: "))
            quantity = int(input("Quantity: "))
            discount = float(input("Discount: "))

            order_details_data.append({
                'productid': productid,
                'unitprice': unitprice,
                'quantity': quantity,
                'discount': discount
            })

        return order_data, order_details_data

    @staticmethod
    def display_order_details(order, details, employee, customer):
        if order:
            print()
            print(f"Order ID: {order.orderid}")
            print(f"Nome do Cliente: {customer.contactname}")
            print(f"Nome da Vendedor: {employee.firstname}")
            print(f"Order Date: {order.orderdate}")
            print("Order Details:")
            for detail in details:
                print(f"Product ID: {detail.productid}, Unit Price: {detail.unitprice}, Quantity: {detail.quantity}")
        else:
            print("Order not found.")
        print()
    @staticmethod
    def display_employee_ranking(ranking):
        print()
        for rank in ranking:
            print(f"Employee: {rank[0]}, Total Orders: {rank[1]}, Total Sales: {rank[2]}")
        print()