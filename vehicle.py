
class Vehicle:
    def __init__(self, vehicle_id, brand, model, rent_per_day):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.rent_per_day = rent_per_day
        self.is_available = True

    def display_details(self):
        print("Vehicle ID:", self.vehicle_id)
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Rent per day:", self.rent_per_day)
        print("Available:", self.is_available)

    def calculate_rent(self, days):
        return self.rent_per_day * days


class Car(Vehicle):
    def calculate_rent(self, days):
        base_amount = self.rent_per_day * days
        insurance = base_amount * 0.10
        return base_amount + insurance


class Bike(Vehicle):
    def calculate_rent(self, days):
        base_amount = self.rent_per_day * days
        helmet_charge = 50
        return base_amount + helmet_charge

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
