from validation import validate_positive_id, validate_non_empty_text, validate_daily_rent


class Vehicle:
    def __init__(self, vehicle_id, brand, model, rent_per_day):
        # These rules apply both to interactive registration and saved-file loading.
        self.vehicle_id = validate_positive_id(vehicle_id, "Vehicle ID")
        self.brand = validate_non_empty_text(brand, "Brand")
        self.model = validate_non_empty_text(model, "Model")
        self.rent_per_day = validate_daily_rent(rent_per_day)
        self.is_available = True

    def display_details(self):
        print("Vehicle ID:", self.vehicle_id)
        print("Brand:", self.brand)
        print("Model:", self.model)
        print(f"Rent per day: ₹{self.rent_per_day:.2f}")
        print("Available:", self.is_available)

    def calculate_price_breakdown(self, days):
        """Return a transparent price breakdown for this vehicle."""
        base_amount = self.rent_per_day * days
        return {
            "base_amount": base_amount,
            "insurance": 0.0,
            "helmet_charge": 0.0,
            "total": base_amount,
        }

    def calculate_rent(self, days):
        # Keep the original method available for existing callers.
        return self.calculate_price_breakdown(days)["total"]


class Car(Vehicle):
    def calculate_price_breakdown(self, days):
        base_amount = self.rent_per_day * days
        insurance = base_amount * 0.10
        return {
            "base_amount": base_amount,
            "insurance": insurance,
            "helmet_charge": 0.0,
            "total": base_amount + insurance,
        }


class Bike(Vehicle):
    def calculate_price_breakdown(self, days):
        base_amount = self.rent_per_day * days
        helmet_charge = 50.0  # One-time helmet charge per booking.
        return {
            "base_amount": base_amount,
            "insurance": 0.0,
            "helmet_charge": helmet_charge,
            "total": base_amount + helmet_charge,
        }

    
'''
car1 = Car(101, "Toyota", "Innova", 2000)
bike1 = Bike(102, "Royal Enfield", "Classic 350", 800)
bike2 = Bike(103, "Yamaha","MT-15",600)

print("Car_1 Details")
car1.display_details()
print("Car rent for 3 days:", car1.calculate_rent(3))
print("\nBike_1 Details")
bike1.display_details()
print("Bike rent for 3 days:", bike1.calculate_rent(3))
print("\nBike_2 Details")
bike2.display_details()
print("Bike rent for 5 days:", bike2.calculate_rent(5))

'''
