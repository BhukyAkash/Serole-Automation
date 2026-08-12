import random

def generate_mykad(gender: str = None) -> str:
    # --- Date of birth ---
    birth_year  = random.randint(1965, 2005)
    birth_month = random.randint(1, 12)

    # Max day per month (simplified: no leap-year edge case needed)
    max_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if birth_month == 2 and (birth_year % 4 == 0):
        max_day = 29
    else:
        max_day = max_days[birth_month]

    birth_day = random.randint(1, max_day)

    yy = str(birth_year)[-2:]
    mm = f"{birth_month:02d}"
    dd = f"{birth_day:02d}"

    # --- Place of birth code (01–16 = Malaysian states) ---
    pb = f"{random.randint(1, 16):02d}"

    # --- Last 4 digits ---
    seq = random.randint(0, 999)
    seq_str = f"{seq:03d}"

    if gender == "male":
        gender_digit = random.choice([1, 3, 5, 7, 9])   # odd
    elif gender == "female":
        gender_digit = random.choice([0, 2, 4, 6, 8])   # even
    else:
        gender_digit = random.randint(0, 9)              # random

    return f"{yy}{mm}{dd}{pb}{seq_str}{gender_digit}"



