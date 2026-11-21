
from datetime import datetime, timedelta


class Booking:

    def __init__(self, booking_id, customer, vehicle, rental_days):

        self.booking_id = booking_id
        self.customer = customer
        self.vehicle = vehicle
        self.rental_days = rental_days

        
        self.booking_date = datetime.now()
        self.due_date = self.booking_date + timedelta(days=rental_days)

        self.actual_return_date = None
        self.status = "CONFIRMED"
        self.final_amount = 0

    def display_booking(self):

        print("\n------- BOOKING DETAILS -------")
        print("Booking ID:", self.booking_id)
        print("Customer:", self.customer.name)
        print("Vehicle:", self.vehicle.brand, self.vehicle.model)
        print("Rental Days:", self.rental_days)
        print("Booking Date:", self.booking_date.strftime("%d-%m-%Y"))
        print("Status:", self.status)


class BookingManagement:

    def __init__(self, vehicles, customers):

        self.vehicles = vehicles
        self.customers = customers
        self.bookings = []
        self.next_booking_id = 1001

    def create_booking(self, customer_id, vehicle_id, rental_days):

        # Validate rental duration
        if not isinstance(rental_days, int) or rental_days <= 0:
            print("Enter a valid rental duration!")
            return

        # Find customer
        customer = None

        for c in self.customers:
            if c.customer_id == customer_id:
                customer = c
                break

        if customer is None:
            print("Customer not found!")
            return

        # Find vehicle
        vehicle = None

        for v in self.vehicles:
            if v.vehicle_id == vehicle_id:
                vehicle = v
                break

        if vehicle is None:
            print("Vehicle not found!")
            return

        # Check availability
        if not vehicle.is_available:
            print("Vehicle is already booked!")
            return

        # Create booking
        booking = Booking(
            self.next_booking_id,
            customer,
            vehicle,
            rental_days
        )

        self.bookings.append(booking)

        # Update vehicle availability
        vehicle.is_available = False

        print("Booking created successfully!")
        print("Booking ID:", self.next_booking_id)

        self.next_booking_id += 1

    def display_bookings(self):

        if not self.bookings:
            print("No bookings available!")
            return

        for booking in self.bookings:
            booking.display_booking()

    def search_booking(self, booking_id):

        for booking in self.bookings:

            if booking.booking_id == booking_id:
                booking.display_booking()
                return booking

        print("Booking not found!")
        return None
