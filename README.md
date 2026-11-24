# Python Vehicle Rental Management System

A menu-driven, console-based vehicle rental application built with Python and object-oriented programming (OOP). The application manages cars, bikes, customers, bookings, vehicle returns, rental charges, and local TXT-file persistence.

## Features

- Register cars and bikes with unique positive vehicle IDs.
- Register customers with validated names, phone numbers, and email addresses.
- Display vehicles and their availability, customers, and booking history.
- Create bookings only for registered customers and available vehicles.
- Generate booking IDs automatically, starting at `1001` and continuing after the highest saved ID.
- Restore vehicle, customer, and booking records when the application starts.
- Preserve booking-to-customer and booking-to-vehicle relationships when loading records.
- Return vehicles using the current date/time or a manually entered return timestamp.
- Show estimated booking prices and final rental summaries with itemized charges.
- Validate interactive input and saved records.
- Protect existing data with staged file writes and rollback if a multi-file save fails.

## Requirements

- Python 3.10 or later recommended.
- Python standard library only. No third-party packages are required.
- The project was syntax-checked and its included test scripts were run with Python 3.13.5.

## Project structure

```text
python_project_vehicle_rental_management/
├── main.py             # Application menu and startup/data-loading workflow
├── vehicle.py          # Vehicle, Car, and Bike classes and price breakdowns
├── customer.py         # Customer model and customer management
├── booking.py          # Booking model and booking management
├── rental.py           # Return processing, duration, late days, and charges
├── validation.py       # Shared input and saved-record validation
├── file_handler.py     # Safe pipe-delimited TXT storage
├── test.py             # Application logic and validation regression checks
├── test_storage.py     # Automated file-storage unit tests
├── README.md
└── data/               # Created/used for local TXT records
    ├── vehicles.txt
    ├── customers.txt
    └── bookings.txt
```

The three TXT files are created when records are saved. The `data` folder is resolved relative to `file_handler.py`, not the terminal's current working directory.

## Run the application

Open a terminal in the project folder and run:

```bash
python main.py
```

The menu supports:

1. Add Vehicle
2. Register Customer
3. Display Vehicles
4. Display Customers
5. Book Vehicle
6. Display Bookings
7. Return Vehicle
8. Exit

## Run the tests

Run both test scripts from the project folder:

```bash
python test.py
python test_storage.py
```

- `test.py` checks return-date validation, successful and duplicate returns, missing booking IDs, price calculations, late charges, and registration validation.
- `test_storage.py` runs seven `unittest` cases covering pipe-delimited reading/writing, missing files, project-relative paths, unsafe field values, validation before replacing files, and rollback after a simulated replacement failure.

Both scripts use only Python's standard library.

## Registration validation

- Vehicle IDs and customer IDs must be positive integers.
- Vehicle brand and model, and customer name, cannot be blank.
- Daily rent must be a finite number greater than zero. Zero, negative values, `NaN`, and infinity are rejected.
- Customer phone numbers must contain exactly 10 digits.
- Customer email addresses must follow the application's basic email format, for example `name@example.com`.
- The same model-level validation is applied when saved TXT records are restored.

## Pricing policy

The application displays the estimate at booking time and a separate itemized final amount when a vehicle is returned.

### Cars

- Base rent = daily rent × charged rental days.
- Insurance = 10% of base rent.
- Estimated/final rental subtotal = base rent + insurance.

### Bikes

- Base rent = daily rent × charged rental days.
- Helmet charge = ₹50 one-time per booking.
- Estimated/final rental subtotal = base rent + helmet charge.

### Late return

- Late charge per day = daily rent × 1.5.
- Late charges = late days × late charge per day.
- Final amount = rental subtotal + late charges.
- Late charges are calculated at return and are not included in the original booking estimate.

All displayed currency amounts use two decimal places.

## Rental duration and due-date policy

- Rental duration is calculated using calendar-date subtraction, with a minimum charge of one day for a valid same-day return.
- A return timestamp earlier than the booking timestamp is rejected.
- The due date is the calendar date reached by adding the booked rental days to the booking date. The vehicle is due by the end of that date.
- A return at any time on the due date is on time. Each calendar date after the due date counts as one late day.
- When returning a vehicle, enter the actual return date/time in `DD-MM-YYYY HH:MM` format, or press Enter to use the current date and time.

## TXT storage and data safety

- Records use Python's `csv` module with `|` as the delimiter.
- Pipe and newline characters are rejected inside fields to protect the record format.
- Before saving, the application validates and stages all three data sets in temporary files.
- The file handler replaces the destination files only after staging succeeds. If a replacement fails, it attempts to restore files already replaced.
- If invalid or inconsistent saved records are detected during startup, those records (and bookings that refer to missing/invalid related records) are skipped and saving is disabled for that session. This protects the original TXT files from being overwritten with incomplete data.
- Back up the `data` folder before manually editing or repairing saved records.

## Helper methods

`search_customer()` and `search_booking()` are available as management helper methods for code-level lookups. They are not separate choices in the current console menu.

## Clone the repository

```bash
git clone https://github.com/koppisettimanoj26-lang/python_project_vehicle_rental_management.git
cd python_project_vehicle_rental_management
python main.py
```

## Notes and limitations

- This is a local, single-user console application. It is intended as a learning/portfolio project, not a multi-user production booking service.
- Runtime customer and booking data are stored locally in the `data` folder. Keep backups if the records matter.
- No authentication, payment gateway, web interface, or remote database is included.
