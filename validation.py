"""Shared validation rules for vehicle and customer data."""

import math
import re


def validate_positive_id(value, field_name="ID"):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer.")
    return value


def validate_non_empty_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_daily_rent(value):
    try:
        rent = float(value)
    except (TypeError, ValueError):
        raise ValueError("Daily rent must be a valid number.")

    if not math.isfinite(rent) or rent <= 0:
        raise ValueError("Daily rent must be a finite number greater than zero.")
    return rent


def validate_phone(phone):
    phone = str(phone).strip()
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Phone number must contain exactly 10 digits.")
    return phone


def validate_email(email):
    email = validate_non_empty_text(email, "Email address")
    # Practical format check: one @, a non-empty local/domain part,
    # and a domain suffix containing at least two letters.
    pattern = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$"
    if not re.fullmatch(pattern, email):
        raise ValueError("Enter a valid email address (example: name@example.com).")
    return email
