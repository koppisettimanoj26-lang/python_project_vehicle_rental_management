
from datetime import datetime


class RentalManagement:

    def __init__(self, bookings):
        self.bookings = bookings

    def calculate_rental_duration(self, booking, return_date):
        """Calculate calendar rental days with a one-day minimum charge.

        A return later on the booking date is valid and is charged as one day.
        A return timestamp earlier than the booking timestamp is rejected.
        """
        if return_date < booking.booking_date:
            raise ValueError("Return date cannot be before the booking date.")

        duration = (return_date.date() - booking.booking_date.date()).days

        # A valid same-day rental is charged for at least one day.
        return max(1, duration)

    def calculate_rental_price(self, booking, actual_days):
        # Polymorphism: each vehicle type supplies its own itemized charges.
        return booking.vehicle.calculate_price_breakdown(actual_days)

    def calculate_late_days(self, booking, return_date):
        """Count calendar dates after the due date as late days.

        The entire due calendar date is included. A return at any time on
        that date is on time; each following calendar date adds one late day.
        """
        return max(0, (return_date.date() - booking.due_date.date()).days)

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
            return False

        if booking.status == "RETURNED":
            print("Vehicle has already been returned!")
            return False

        if return_date is None:
            return_date = datetime.now()
        elif not isinstance(return_date, datetime):
            print("Invalid return date. Please provide a valid datetime value.")
            return False

        # Calculate actual rental duration
        try:
            actual_days = self.calculate_rental_duration(
                booking, return_date
            )

        except ValueError as error:
            print(error)
            return False

        # Calculate late days using the same calendar-date policy as duration.
        late_days = self.calculate_late_days(booking, return_date)

        # Calculate rental amount
        price_breakdown = self.calculate_rental_price(booking, actual_days)
        rental_amount = price_breakdown["total"]

        # Calculate late charges separately from the rental/vehicle add-ons.
        late_charges = self.calculate_late_charges(booking, late_days)

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
        print("Booking Date:", booking.booking_date.strftime("%d-%m-%Y %H:%M"))
        print("Due Date:", booking.due_date.strftime("%d-%m-%Y"), "(end of day)")
        print("Actual Return Date:", return_date.strftime("%d-%m-%Y %H:%M"))
        print("Actual Rental Days:", actual_days)
        print("Late Days:", late_days)
        print("\nPrice Breakdown:")
        print(
            f"  Base Rent ({actual_days} day(s) × "
            f"₹{booking.vehicle.rent_per_day:.2f}): "
            f"₹{price_breakdown['base_amount']:.2f}"
        )
        if price_breakdown["insurance"]:
            print(f"  Insurance (10% of base rent): ₹{price_breakdown['insurance']:.2f}")
        if price_breakdown["helmet_charge"]:
            print(f"  Helmet Charge (one-time): ₹{price_breakdown['helmet_charge']:.2f}")
        print(f"  Rental Subtotal: ₹{rental_amount:.2f}")
        print(
            f"  Late Charges ({late_days} day(s) × "
            f"₹{booking.vehicle.rent_per_day * 1.5:.2f}): "
            f"₹{late_charges:.2f}"
        )
        print(f"Final Amount: ₹{final_amount:.2f}")

        # The caller must save the updated records before reporting success.
        return True
