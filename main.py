from controller.controller import OrderController

def main():
    dao_choice = input("Escolha o método de acesso (psycopg/sqlalchemy): ").strip().lower()
    
    if dao_choice not in ['psycopg', 'sqlalchemy']:
        print("Escolha inválida, fechando o programa...")
        return
    
    controller = OrderController(dao_choice)
    
    while True:
        print("1. Create Order")
        print("2. Show Order Details")
        print("3. Show Employee Ranking")
        print("4. Exit")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            controller.create_order()
        elif choice == '2':
            order_id = input("Enter Order ID: ")
            controller.show_order_details(order_id)
        elif choice == '3':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            controller.show_employee_ranking(start_date, end_date)
        elif choice == '4':
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
