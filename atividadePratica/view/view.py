# view/view.py

class OrderView:
    @staticmethod
    def get_order_input():
        order_id = input("Order ID: ")
        customer_id = input("Customer ID: ")
        employee_id = input("Employee ID: ")
        order_date = input("Order Date (YYYY-MM-DD): ")
        required_date = input("Required Date (YYYY-MM-DD): ")
        shipped_date = input("Shipped Date (YYYY-MM-DD): ")
        freight = float(input("Freight: "))
        ship_name = input("Ship Name: ")
        ship_address = input("Ship Address: ")
        ship_city = input("Ship City: ")
        ship_region = input("Ship Region: ")
        ship_postal_code = input("Ship Postal Code: ")
        ship_country = input("Ship Country: ")
        shipper_id = int(input("Shipper ID: "))
        
        order_data = {
            'order_id': order_id, 
            'customer_id': customer_id,
            'employee_id': employee_id,
            'order_date': order_date,
            'required_date': required_date,
            'shipped_date': shipped_date,
            'freight': freight,
            'ship_name': ship_name,
            'ship_address': ship_address,
            'ship_city': ship_city,
            'ship_region': ship_region,
            'ship_postal_code': ship_postal_code,
            'ship_country': ship_country,
            'shipper_id': shipper_id
        }

        order_details_data = []
        while True:
            product_id = input("Product ID (or 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            unit_price = float(input("Unit Price: "))
            quantity = int(input("Quantity: "))
            discount = float(input("Discount: "))

            order_details_data.append({
                'product_id': product_id,
                'unit_price': unit_price,
                'quantity': quantity,
                'discount': discount
            })

            more = input("Add more items? (y/n): ")
            if more.lower() != 'y':
                break
        
        return order_data, order_details_data

    @staticmethod
    def display_order_details(order, details):
        if order:
            print(f"Order ID: {order.order_id}")
            print(f"Order Date: {order.order_date}")
            print(f"Required Date: {order.required_date}")
            print(f"Shipped Date: {order.shipped_date}")
            print(f"Freight: {order.freight}")
            print(f"Ship Name: {order.ship_name}")
            print(f"Ship Address: {order.ship_address}")
            print(f"Ship City: {order.ship_city}")
            print(f"Ship Region: {order.ship_region}")
            print(f"Ship Postal Code: {order.ship_postal_code}")
            print(f"Ship Country: {order.ship_country}")
            print(f"Shipper ID: {order.shipper_id}")
            print("Order Details:")
            for detail in details:
                print(f" - Product ID: {detail.product_id}, Unit Price: {detail.unit_price}, Quantity: {detail.quantity}, Discount: {detail.discount}")
        else:
            print("Order not found.")

    @staticmethod
    def display_employee_ranking(ranking):
        for rank in ranking:
            print(f"Employee: {rank.first_name} {rank.last_name}, Total Orders: {rank.total_orders}, Total Sales: {rank.total_sales}")
