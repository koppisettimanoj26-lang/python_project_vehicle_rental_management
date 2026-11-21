# 🚗 Vehicle Rental Management System

## 📌 Project Overview

The **Vehicle Rental Management System** is a console-based Python application developed using Object-Oriented Programming (OOP) concepts. It helps manage vehicle rentals by allowing users to add vehicles, register customers, create bookings, calculate rental charges, and process vehicle returns.

The project demonstrates practical Python programming concepts, including classes, objects, inheritance, polymorphism, method overriding, exception handling, and file handling.

## ✨ Features

- **Vehicle Management**
  - Add cars and bikes.
  - Display vehicle details.
  - Check vehicle availability.
- **Customer Management**
  - Register new customers.
  - Validate customer details.
  - Search customers by ID.
- **Booking Management**
  - Create vehicle bookings.
  - Generate unique booking IDs.
  - Prevent booking unavailable vehicles.
  - Display and search bookings.
- **Rental Management**
  - Calculate rental duration.
  - Calculate rental charges.
  - Apply late return charges.
  - Process vehicle returns.
  - Update vehicle availability.
- **Exception Handling**
  - Handle invalid booking IDs.
  - Prevent duplicate vehicle returns.
  - Validate return dates.
- **File Handling**
  - Store application records in TXT files.
  - Read and write data using Python file operations.

## 🛠️ Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- File Handling (TXT)
- Exception Handling
- Python Modules

## 📂 Project Structure

```text
Vehicle_Rental_System/
│
├── main.py
├── vehicle.py
├── customer.py
├── booking.py
├── rental.py
├── file_handler.py
├── exceptions.py
│
└── data/
    ├── vehicles.txt
    ├── customers.txt
    └── bookings.txt
```

## 🧠 Python Concepts Implemented

| Concept | Implementation |
|---|---|
| Classes and Objects | Vehicle, Customer, Booking |
| Inheritance | Car and Bike inherit from Vehicle |
| Polymorphism | Different rental calculations for cars and bikes |
| Method Overriding | Car and Bike override `calculate_rent()` |
| Encapsulation | Organizing data and methods inside classes |
| Exception Handling | Custom exceptions and try-except blocks |
| File Handling | Reading and writing TXT files |
| Modules | Separating functionality into Python files |

## 💰 Rental Calculation

Different vehicle types have different rental calculations.

**Car:**
- Base rental amount = Rent per day × Rental days
- Insurance charge = 10% of base rental amount
- Total = Base amount + Insurance

**Bike:**
- Base rental amount = Rent per day × Rental days
- Helmet charge = ₹50
- Total = Base amount + Helmet charge

**Late Return Charges:**

- Late charge per day = 1.5 × Vehicle rent per day
- Total late charge = Late days × Late charge per day

## ▶️ How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd Vehicle_Rental_System
```

### 3. Run the application

```bash
python main.py
```

### 4. Follow the menu

Choose the required option to manage vehicles, customers, bookings, and returns.

## 🎯 Project Objectives

- Develop a real-world application using Python.
- Understand and implement OOP principles.
- Practice inheritance and polymorphism.
- Implement exception handling for invalid operations.
- Understand file handling and modular programming.
- Improve problem-solving and application development skills.

## 🚀 Future Enhancements

- Implement complete data loading and persistence after application restart.
- Add a graphical user interface (GUI).
- Integrate a MySQL database.
- Generate rental invoices.
- Add customer login and authentication.
- Develop a web application using Flask or Django.

## 👨‍💻 Author

**Manoj Kumar**

- GitHub: [koppisettimanoj26-lang](https://github.com/koppisettimanoj26-lang)

---

⭐ If you find this project useful, feel free to star the repository!
