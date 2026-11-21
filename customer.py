class Customer:

    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email

    def display_details(self):
        print("\n----- CUSTOMER DETAILS -----")
        print("Customer ID:", self.customer_id)
        print("Name:", self.name)
        print("Phone:", self.phone)
        print("Email:", self.email)

class CustomerManagement:

    def __init__(self):
        self.customers = []

    def register_customer(self, customer):
        for existing_customer in self.customers:

            if existing_customer.customer_id == customer.customer_id:
                print("Customer ID already exists!")
                return

        if not customer.name.strip():
            print("Customer name cannot be empty!")
            return

        if not customer.phone.isdigit() or len(customer.phone) != 10:
            print("Enter a valid 10-digit phone number!")
            return

        if "@" not in customer.email or "." not in customer.email:
            print("Enter a valid email address!")
            return

        self.customers.append(customer)
        print("Customer registered successfully!")

    def display_customers(self):
        if not self.customers:
            print("No customers registered.")
            return

        for customer in self.customers:
            customer.display_details()

    def search_customer(self, customer_id):
        for customer in self.customers:

            if customer.customer_id == customer_id:
                customer.display_details()
                return customer

        print("Customer not found!")
        return None

'''
customer1 = Customer(1,"Manoj","9052935056","manoj123@gmail.com")
customer2 = Customer(2,"Teja","8919560943","teja123@gmail.com")
customer1.display_details()



management = CustomerManagement()
management.register_customer(customer1)
management.register_customer(customer2)

management.display_customers()
'''
