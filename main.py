import math
from vehicle import Car, Bike
from customer import Customer, CustomerManagement
from booking import Booking, BookingManagement
from rental import RentalManagement
from file_handler import FileHandler
from datetime import datetime
from validation import validate_positive_id, validate_non_empty_text, validate_daily_rent

# Initialize application
handler = FileHandler()

vehicles = []
customer_manager = CustomerManagement()
booking_manager = BookingManagement(vehicles, customer_manager.customers)
rental_manager = RentalManagement(booking_manager.bookings)

# Saving is disabled if existing files contain damaged or inconsistent records.
# This prevents a later Exit from overwriting the original files with partial data.
persistence_safe = True


def parse_saved_bool(value, field_name):
    value = str(value).strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(f"Invalid {field_name} value: {value!r}; expected True or False")


def load_all():
    """Load valid records individually while preserving files containing bad rows."""
    global persistence_safe

    try:
        vehicle_rows = handler.load_data("vehicles.txt")
        customer_rows = handler.load_data("customers.txt")
        booking_rows = handler.load_data("bookings.txt")
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        persistence_safe = False
        print("\\nDATA LOAD WARNING:", error)
        print("Existing TXT files have been preserved.")
        print("Saving is disabled for this session to prevent overwriting damaged data.")
        return

    loaded_vehicles = []
    vehicle_lookup = {}

    # Load each vehicle independently. A bad row must not block valid rows.
    for line_no, row in enumerate(vehicle_rows, start=1):
        try:
            if len(row) != 6:
                raise ValueError(f"expected 6 fields, found {len(row)}")

            vehicle_id = int(row[0])
            vehicle_type = row[1].strip().lower()
            brand, model = row[2], row[3]
            rent_per_day = validate_daily_rent(row[4])
            is_available = parse_saved_bool(row[5], "vehicle availability")

            validate_positive_id(vehicle_id, "Vehicle ID")
            validate_non_empty_text(brand, "Brand")
            validate_non_empty_text(model, "Model")

            if vehicle_id in vehicle_lookup:
                raise ValueError(f"duplicate vehicle ID {vehicle_id}")

            if vehicle_type == "car":
                vehicle = Car(vehicle_id, brand, model, rent_per_day)
            elif vehicle_type == "bike":
                vehicle = Bike(vehicle_id, brand, model, rent_per_day)
            else:
                raise ValueError(f"unknown vehicle type {row[1]!r}")

            vehicle.is_available = is_available
            loaded_vehicles.append(vehicle)
            vehicle_lookup[vehicle_id] = vehicle
        except (ValueError, TypeError) as error:
            persistence_safe = False
            print(f"INVALID DATA: vehicles.txt line {line_no}: {error}. Record skipped.")

    loaded_customers = []
    customer_lookup = {}

    # Customers are also validated independently.
    for line_no, row in enumerate(customer_rows, start=1):
        try:
            if len(row) != 4:
                raise ValueError(f"expected 4 fields, found {len(row)}")

            customer_id = int(row[0])
            customer = Customer(customer_id, row[1], row[2], row[3])
            if customer_id in customer_lookup:
                raise ValueError(f"duplicate customer ID {customer_id}")

            loaded_customers.append(customer)
            customer_lookup[customer_id] = customer
        except (ValueError, TypeError) as error:
            persistence_safe = False
            print(f"INVALID DATA: customers.txt line {line_no}: {error}. Record skipped.")

    loaded_bookings = []
    active_vehicle_ids = set()
    booking_ids = set()

    # Bookings are loaded last so references can be checked against valid records.
    for line_no, row in enumerate(booking_rows, start=1):
        try:
            if len(row) not in {9, 10}:
                raise ValueError(f"expected 9 or 10 fields, found {len(row)}")

            booking_id = int(row[0])
            customer_id = int(row[1])
            vehicle_id = int(row[2])
            rental_days = int(row[3])

            validate_positive_id(booking_id, "Booking ID")
            if rental_days <= 0:
                raise ValueError("rental days must be positive")
            if booking_id in booking_ids:
                raise ValueError(f"duplicate booking ID {booking_id}")
            if customer_id not in customer_lookup:
                raise ValueError(f"customer ID {customer_id} does not exist or was invalid")
            if vehicle_id not in vehicle_lookup:
                raise ValueError(f"vehicle ID {vehicle_id} does not exist or was invalid")

            booking_date = datetime.fromisoformat(row[4])
            due_date = datetime.fromisoformat(row[5])
            actual_return_date = datetime.fromisoformat(row[6]) if row[6].strip() else None
            status = row[7].strip().upper()
            final_amount = float(row[8]) if row[8].strip() else 0.0

            if status not in {"CONFIRMED", "RETURNED", "CANCELLED", "PENDING"}:
                raise ValueError(f"invalid status {status!r}")
            if not math.isfinite(final_amount) or final_amount < 0:
                raise ValueError("final amount must be finite and non-negative")
            if status == "RETURNED" and actual_return_date is None:
                raise ValueError("returned booking has no actual return date")

            booking = Booking(
                booking_id, customer_lookup[customer_id],
                vehicle_lookup[vehicle_id], rental_days
            )
            booking.booking_date = booking_date
            booking.due_date = due_date
            booking.actual_return_date = actual_return_date
            booking.status = status
            booking.final_amount = final_amount

            if len(row) == 10 and row[9].strip():
                booking.estimated_amount = float(row[9])
            if (not math.isfinite(booking.estimated_amount)
                    or booking.estimated_amount < 0):
                raise ValueError("estimated amount must be finite and non-negative")

            if status in {"CONFIRMED", "PENDING"}:
                if vehicle_id in active_vehicle_ids:
                    raise ValueError(f"vehicle {vehicle_id} has multiple active bookings")
                active_vehicle_ids.add(vehicle_id)

            loaded_bookings.append(booking)
            booking_ids.add(booking_id)
        except (ValueError, TypeError, OverflowError) as error:
            persistence_safe = False
            print(f"INVALID DATA: bookings.txt line {line_no}: {error}. Record skipped.")

    for vehicle_id in active_vehicle_ids:
        vehicle_lookup[vehicle_id].is_available = False

    vehicles.extend(loaded_vehicles)
    customer_manager.customers.extend(loaded_customers)
    booking_manager.bookings.extend(loaded_bookings)
    booking_manager.next_booking_id = max(booking_ids, default=1000) + 1

    print(
        f"Loaded {len(loaded_vehicles)} valid vehicle(s), "
        f"{len(loaded_customers)} valid customer(s), "
        f"and {len(loaded_bookings)} valid booking(s)."
    )

    if not persistence_safe:
        print("DATA LOAD WARNING: One or more invalid records were skipped.")
        print("Original TXT files have been preserved.")
        print("Saving is disabled for this session to prevent overwriting damaged data.")


# Save current records
def save_all():
    if not persistence_safe:
        print("Save cancelled: existing data could not be loaded safely.")
        return False

    vehicle_records = []
    for v in vehicles:
        vehicle_type = "Car" if isinstance(v, Car) else "Bike"
        vehicle_records.append([
            v.vehicle_id, vehicle_type, v.brand, v.model,
            v.rent_per_day, v.is_available
        ])

    customer_records = []
    for c in customer_manager.customers:
        customer_records.append([c.customer_id, c.name, c.phone, c.email])

    booking_records = []
    for b in booking_manager.bookings:
        booking_records.append([
            b.booking_id,
            b.customer.customer_id,
            b.vehicle.vehicle_id,
            b.rental_days,
            b.booking_date.isoformat(),
            b.due_date.isoformat(),
            b.actual_return_date.isoformat() if b.actual_return_date else "",
            b.status,
            b.final_amount,
            b.estimated_amount
        ])

    # Validate the complete in-memory snapshot before changing any TXT file.
    try:
        for record in vehicle_records:
            if len(record) != 6:
                raise ValueError("Vehicle record must contain exactly 6 fields.")
            validate_positive_id(record[0], "Vehicle ID")
            validate_non_empty_text(record[2], "Brand")
            validate_non_empty_text(record[3], "Model")
            validate_daily_rent(record[4])
            if not isinstance(record[5], bool):
                raise ValueError("Vehicle availability must be True or False.")

        for record in customer_records:
            if len(record) != 4:
                raise ValueError("Customer record must contain exactly 4 fields.")
            validate_positive_id(record[0], "Customer ID")
            # Reuse the Customer constructor's shared field validation.
            Customer(*record)

        valid_customer_ids = {record[0] for record in customer_records}
        valid_vehicle_ids = {record[0] for record in vehicle_records}
        for record in booking_records:
            if len(record) != 10:
                raise ValueError("Booking record must contain exactly 10 fields.")
            validate_positive_id(record[0], "Booking ID")
            if record[1] not in valid_customer_ids:
                raise ValueError("Booking references a missing customer.")
            if record[2] not in valid_vehicle_ids:
                raise ValueError("Booking references a missing vehicle.")
            if not isinstance(record[3], int) or record[3] <= 0:
                raise ValueError("Booking rental days must be a positive integer.")
            if not math.isfinite(float(record[8])) or float(record[8]) < 0:
                raise ValueError("Booking final amount must be finite and non-negative.")
            if not math.isfinite(float(record[9])) or float(record[9]) < 0:
                raise ValueError("Booking estimated amount must be finite and non-negative.")

        handler.save_many({
            "vehicles.txt": vehicle_records,
            "customers.txt": customer_records,
            "bookings.txt": booking_records,
        })
        return True
    except (OSError, ValueError, TypeError, OverflowError) as error:
        print("Could not save data:", error)
        return False


def display_vehicles():
    if not vehicles:
        print("No vehicles registered!")
        return
    for v in vehicles:
        v.display_details()


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
                validate_positive_id(vehicle_id, "Vehicle ID")
                vehicle_type = input("Enter type (Car/Bike): ").strip().lower()
                brand = validate_non_empty_text(input("Enter brand: "), "Brand")
                model = validate_non_empty_text(input("Enter model: "), "Model")
                rent = validate_daily_rent(input("Enter daily rent: "))
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
                if save_all():
                    print("Vehicle added successfully!")

            elif choice == 2:
                customer_id = int(input("Enter customer ID: "))
                validate_positive_id(customer_id, "Customer ID")
                name = input("Enter name: ")
                phone = input("Enter phone: ")
                email = input("Enter email: ")
                customer = Customer(customer_id, name, phone, email)
                old_count = len(customer_manager.customers)
                customer_manager.register_customer(customer)
                if len(customer_manager.customers) > old_count:
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
                booking_manager.create_booking(customer_id, vehicle_id, days)
                if len(booking_manager.bookings) > old_count:
                    created_booking = booking_manager.bookings[-1]
                    if save_all():
                        print(f"Estimated Booking Amount: ₹{created_booking.estimated_amount:.2f}")
            elif choice == 6:
                booking_manager.display_bookings()
            elif choice == 7:
                booking_id = int(input("Enter booking ID: "))

                # Keep the original state so it can be restored if saving fails.
                booking = next(
                    (b for b in booking_manager.bookings
                     if b.booking_id == booking_id),
                    None
                )

                if booking is None:
                    rental_manager.return_vehicle(booking_id)
                    continue

                old_status = booking.status
                old_return_date = booking.actual_return_date
                old_final_amount = booking.final_amount
                old_vehicle_availability = booking.vehicle.is_available

                return_input = input(
                    "Enter actual return date and time (DD-MM-YYYY HH:MM), "
                    "or press Enter for now: "
                ).strip()

                if return_input:
                    try:
                        return_date = datetime.strptime(
                            return_input, "%d-%m-%Y %H:%M"
                        )
                    except ValueError:
                        print(
                            "Invalid date format. Use DD-MM-YYYY HH:MM "
                            "(example: 23-11-2026 18:30)."
                        )
                        continue
                else:
                    return_date = datetime.now()

                result = rental_manager.return_vehicle(booking_id, return_date)

                if result:
                    if save_all():
                        print("Vehicle return saved successfully!")
                    else:
                        # Do not leave the in-memory state ahead of the TXT files.
                        booking.status = old_status
                        booking.actual_return_date = old_return_date
                        booking.final_amount = old_final_amount
                        booking.vehicle.is_available = old_vehicle_availability
                        print(
                            "Return was not saved. The booking and vehicle "
                            "have been restored to their previous state."
                        )
            elif choice == 8:
                save_all()
                print("Thank you for using Vehicle Rental System!")
                break
            else:
                print("Invalid choice! Select 1 to 8.")

        except ValueError as error:
            print("Invalid input:", error)
        except Exception as error:
            print("Something went wrong:", error)


if __name__ == "__main__":
    load_all()
    main()
