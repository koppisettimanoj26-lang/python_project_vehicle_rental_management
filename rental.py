
from datetime import datetime


class RentalManagement:

    def __init__(self, bookings):
        self.bookings = bookings

    def calculate_rental_duration(self, booking, return_date):

        duration = (return_date.date() - booking.booking_date.date()).days

        if duration < 1:
            raise ValueError("Return date must be at least one day after booking.")

        return duration

    def calculate_rental_price(self, booking, actual_days):

        # Polymorphism: Car and Bike have different methods
        return booking.vehicle.calculate_rent(actual_days)

    def calculate_late_charges(self, booking, late_days):

        late_charge_per_day = booking.vehicle.rent_per_day * 1.5

        return late_charge_per_day * late_days

    def return_vehicle(self, booking_id, return_date=None):

        # Find booking
        booking = None

        for b in self.bookings:

            if b.booking_id == booking_id:
                booking = b
                break

        if booking is None:
            print("Booking not found!")
            return

        if booking.status == "RETURNED":
            print("Vehicle has already been returned!")
            return

        if return_date is None:
            return_date = datetime.now()

        # Calculate actual rental duration
        try:
            actual_days = self.calculate_rental_duration(
                booking, return_date
            )

        except ValueError as error:
            print(error)
            return

        # Calculate late days
        late_days = max(
            0,
            (return_date.date() - booking.due_date.date()).days
        )

        # Calculate rental amount
        rental_amount = self.calculate_rental_price(
            booking, actual_days
        )

        # Calculate late charges
        late_charges = self.calculate_late_charges(
            booking, late_days
        )

        # Final amount
        final_amount = rental_amount + late_charges

        # Update booking
        booking.actual_return_date = return_date
        booking.final_amount = final_amount
        booking.status = "RETURNED"

        # Make vehicle available again
        booking.vehicle.is_available = True

        # Display summary
        print("\n------- RENTAL SUMMARY -------")
        print("Booking ID:", booking.booking_id)
        print("Customer:", booking.customer.name)
        print("Vehicle:", booking.vehicle.model)
        print("Actual Rental Days:", actual_days)
        print("Late Days:", late_days)
        print("Rental Amount: ₹", rental_amount)
        print("Late Charges: ₹", late_charges)
        print("Final Amount: ₹", final_amount)
        print("Vehicle returned successfully!")
