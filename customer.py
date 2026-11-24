from validation import (
    validate_positive_id,
    validate_non_empty_text,
    validate_phone,
    validate_email,
)


class Customer:

    def __init__(self, customer_id, name, phone, email):
        # Shared constructor validation also protects records loaded from TXT.
        self.customer_id = validate_positive_id(customer_id, "Customer ID")
        self.name = validate_non_empty_text(name, "Customer name")
        self.phone = validate_phone(phone)
        self.email = validate_email(email)

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
        try:
            # Re-check at the management boundary in case an object was modified.
            validate_positive_id(customer.customer_id, "Customer ID")
            validate_non_empty_text(customer.name, "Customer name")
            validate_phone(customer.phone)
            validate_email(customer.email)
        except ValueError as error:
            print(error)
            return

        for existing_customer in self.customers:
            if existing_customer.customer_id == customer.customer_id:
                print("Customer ID already exists!")
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
