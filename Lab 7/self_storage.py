import math


def _to_finite_float(value):
    """Convert a string to a finite float, or return None if that's not possible."""
    try:
        number = float(value.strip())
    except (ValueError, TypeError, AttributeError, OverflowError):
        return None
    if not math.isfinite(number):
        return None
    return number


def parse_rental(text):
    """Parse 'unit:months' into (Unit, months). Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    unit, months = parts
    unit = unit.strip()
    if not unit:
        return None
    months_value = _to_finite_float(months)
    if months_value is None or months_value < 0:
        return None
    return unit.title(), months_value


def duration_average(months_csv):
    """Integer average of comma-separated month values. Returns None for invalid input."""
    if not isinstance(months_csv, str):
        return None
    values = []
    for raw in months_csv.split(','):
        raw = raw.strip()
        if not raw:
            return None
        try:
            value = int(raw)
        except ValueError:
            return None
        if value < 0:
            return None
        values.append(value)
    if not values:
        return None
    return sum(values) // len(values)


def payable_rent(text):
    """Rent with 18% tax minus discount, floored at 0. Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    rent = _to_finite_float(parts[0])
    discount = _to_finite_float(parts[1])
    if rent is None or discount is None or rent < 0 or discount < 0:
        return None
    total = rent * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    print("==== Running parse_rental ====")
    user_input = input("Enter unit:months (e.g. medium:6): ")
    result = parse_rental(user_input)
    if result is None:
        print("Invalid input: expected format unit:months (e.g. medium:6)")
    else:
        print("Unit and Months:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter rental months as CSV (e.g. 3,6,12): ")
    result = duration_average(user_input)
    if result is None:
        print("Invalid input: expected non-negative whole numbers separated by commas")
    else:
        print("Average Duration:", result)

    print("\n==== Running payable_rent ====")
    user_input = input("Enter rent|discount (e.g. 2400|200): ")
    result = payable_rent(user_input)
    if result is None:
        print("Invalid input: expected format rent|discount (e.g. 2400|200)")
    else:
        print("Payable Rent:", result)


if __name__ == "__main__":
    main()
