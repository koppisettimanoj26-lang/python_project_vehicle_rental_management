
from datetime import datetime, timedelta

from vehicle import Car
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

# Return vehicle after 5 days
return_date = (
    booking_manager.bookings[0].booking_date
    + timedelta(days=5)
)

print("\nTEST 1: Valid return")
rental_manager.return_vehicle(1001, return_date)

print("\nTEST 2: Duplicate return")
rental_manager.return_vehicle(1001, return_date)

print("\nTEST 3: Invalid booking ID")
rental_manager.return_vehicle(9999)

print("\nTEST 4: Invalid return date")
rental_manager.return_vehicle(
    1001,
    datetime.now() - timedelta(days=10)
)

print("\nVehicle availability:", car1.is_available)
