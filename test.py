
from datetime import datetime, timedelta

from vehicle import Car, Bike
from customer import Customer
from booking import BookingManagement
from rental import RentalManagement

# Create vehicle
car1 = Car(101, "Toyota", "Innova", 2000)
vehicles = [car1]

# Create customer
customer1 = Customer(
    1, "Manoj", "9876543210", "manoj@gmail.com"
)
customers = [customer1]

# Create booking
booking_manager = BookingManagement(vehicles, customers)

booking_manager.create_booking(1, 101, 3)

# Create rental manager
rental_manager = RentalManagement(
    booking_manager.bookings
)

# Keep the booking active while checking that an earlier return timestamp is rejected.
booking = booking_manager.bookings[0]
invalid_return_date = booking.booking_date - timedelta(days=1)

print("\nTEST 1: Invalid return date")
invalid_result = rental_manager.return_vehicle(1001, invalid_return_date)
assert invalid_result is False
assert booking.status == "CONFIRMED"
assert car1.is_available is False
print("Invalid return date was rejected without changing the booking.")

# Return the same booking after five calendar days.
return_date = booking.booking_date + timedelta(days=5)

print("\nTEST 2: Valid return")
valid_result = rental_manager.return_vehicle(1001, return_date)
assert valid_result is True
assert booking.status == "RETURNED"
assert car1.is_available is True

print("\nTEST 3: Duplicate return")
duplicate_result = rental_manager.return_vehicle(1001, return_date)
assert duplicate_result is False

print("\nTEST 4: Invalid booking ID")
missing_result = rental_manager.return_vehicle(9999)
assert missing_result is False

print("\nVehicle availability:", car1.is_available)

# STEP 4: Itemized price calculation tests
print("\nTEST 5: Car price breakdown")
car_breakdown = car1.calculate_price_breakdown(4)
assert car_breakdown["base_amount"] == 8000.0
assert car_breakdown["insurance"] == 800.0
assert car_breakdown["helmet_charge"] == 0.0
assert car_breakdown["total"] == 8800.0
print("Car breakdown passed:", car_breakdown)

print("\nTEST 6: Bike price breakdown")
bike1 = Bike(102, "Honda", "Activa", 800)
bike_breakdown = bike1.calculate_price_breakdown(3)
assert bike_breakdown["base_amount"] == 2400.0
assert bike_breakdown["insurance"] == 0.0
assert bike_breakdown["helmet_charge"] == 50.0
assert bike_breakdown["total"] == 2450.0
print("Bike breakdown passed:", bike_breakdown)

print("\nTEST 7: Late charge calculation")
assert rental_manager.calculate_late_charges(booking_manager.bookings[0], 2) == 6000.0
print("Late charge calculation passed.")


# STEP 5: Registration validation tests
from validation import validate_daily_rent

print("\nTEST 8: Valid vehicle and customer registration data")
assert Car(201, " Toyota ", " Innova ", "2500").brand == "Toyota"
assert Customer(2, " Teja ", "9876543210", "teja@example.com").name == "Teja"
print("Valid registration data passed.")

def must_reject(label, callback):
    try:
        callback()
    except ValueError:
        print(label, "passed.")
    else:
        raise AssertionError(label + " was incorrectly accepted")

print("\nTEST 9: Invalid vehicle and customer data")
must_reject("Empty brand", lambda: Car(202, "   ", "City", 1000))
must_reject("Empty model", lambda: Car(203, "Honda", "  ", 1000))
must_reject("Zero rent", lambda: Car(204, "Honda", "City", 0))
must_reject("Negative rent", lambda: Car(205, "Honda", "City", -100))
must_reject("NaN rent", lambda: Car(206, "Honda", "City", "nan"))
must_reject("Infinite rent", lambda: Bike(207, "Honda", "Activa", "inf"))
must_reject("Non-positive vehicle ID", lambda: Car(0, "Honda", "City", 1000))
must_reject("Non-positive customer ID", lambda: Customer(-1, "Manoj", "9876543210", "m@example.com"))
must_reject("Invalid email", lambda: Customer(3, "Manoj", "9876543210", "manoj@invalid"))
must_reject("Invalid phone", lambda: Customer(4, "Manoj", "123", "m@example.com"))
print("All Step 5 validation tests passed.")
