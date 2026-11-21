
from vehicle import Car, Bike
from customer import Customer, CustomerManagement
from booking import BookingManagement
from rental import RentalManagement
from file_handler import FileHandler

# Initialize application
handler = FileHandler()

vehicles = []
customer_manager = CustomerManagement()
booking_manager = BookingManagement(
    vehicles, customer_manager.customers
)
rental_manager = RentalManagement(booking_manager.bookings)


# Save current records
def save_all():

    vehicle_records = []

    for v in vehicles:
        vehicle_type = "Car" if isinstance(v, Car) else "Bike"

        vehicle_records.append([
            v.vehicle_id,
            vehicle_type,
            v.brand,
            v.model,
            v.rent_per_day,
            v.is_available
        ])

    customer_records = []

    for c in customer_manager.customers:
        customer_records.append([
            c.customer_id,
            c.name,
            c.phone,
            c.email
        ])

    booking_records = []

    for b in booking_manager.bookings:
        booking_records.append([
            b.booking_id,
            b.customer.customer_id,
            b.vehicle.vehicle_id,
            b.rental_days,
            b.booking_date.isoformat(),
            b.due_date.isoformat(),
            b.actual_return_date.isoformat()
                if b.actual_return_date else "",
            b.status,
            b.final_amount
        ])

    handler.save_data("vehicles.txt", vehicle_records)
    handler.save_data("customers.txt", customer_records)
    handler.save_data("bookings.txt", booking_records)


# Display vehicles
def display_vehicles():

    if not vehicles:
        print("No vehicles registered!")
        return

    for v in vehicles:
        v.display_details()


# Main menu
def main():

    while True:

        print("\n===== VEHICLE RENTAL SYSTEM =====")
        print("1. Add Vehicle")
        print("2. Register Customer")
        print("3. Display Vehicles")
        print("4. Display Customers")
        print("5. Book Vehicle")
        print("6. Display Bookings")
        print("7. Return Vehicle")
        print("8. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:

                vehicle_id = int(input("Enter vehicle ID: "))
                vehicle_type = input("Enter type (Car/Bike): ").strip().lower()
                brand = input("Enter brand: ")
                model = input("Enter model: ")
                rent = float(input("Enter daily rent: "))

                if rent <= 0:
                    print("Rent must be positive!")
                    continue

                if vehicle_type == "car":
                    vehicle = Car(vehicle_id, brand, model, rent)

                elif vehicle_type == "bike":
                    vehicle = Bike(vehicle_id, brand, model, rent)

                else:
                    print("Invalid vehicle type!")
                    continue

                if any(v.vehicle_id == vehicle_id for v in vehicles):
                    print("Vehicle ID already exists!")
                    continue

                vehicles.append(vehicle)
                save_all()
                print("Vehicle added successfully!")

            elif choice == 2:

                customer_id = int(input("Enter customer ID: "))
                name = input("Enter name: ")
                phone = input("Enter phone: ")
                email = input("Enter email: ")

                customer = Customer(
                    customer_id, name, phone, email
                )

                customer_manager.register_customer(customer)
                save_all()

            elif choice == 3:

                display_vehicles()

            elif choice == 4:

                customer_manager.display_customers()

            elif choice == 5:

                customer_id = int(input("Enter customer ID: "))
                vehicle_id = int(input("Enter vehicle ID: "))
                days = int(input("Enter rental days: "))

                old_count = len(booking_manager.bookings)

                booking_manager.create_booking(
                    customer_id, vehicle_id, days
                )

                if len(booking_manager.bookings) > old_count:
                    save_all()

            elif choice == 6:

                booking_manager.display_bookings()

            elif choice == 7:

                booking_id = int(input("Enter booking ID: "))

                result = rental_manager.return_vehicle(booking_id)

                if result:
                    save_all()

            elif choice == 8:

                save_all()
                print("Thank you for using Vehicle Rental System!")
                break

            else:
                print("Invalid choice! Select 1 to 8.")

        except ValueError:
            print("Please enter a valid numeric value!")

        except Exception as error:
            print("Something went wrong:", error)


if __name__ == "__main__":
    main()
