def is_leap_year(year):
    """
    Checks if a given year is a leap year.
    """
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

if __name__ == "__main__":
    try:
        y = int(input("Enter a year to check: "))
        if is_leap_year(y):
            print(f"{y} is a leap year!")
        else:
            print(f"{y} is not a leap year.")
    except ValueError:
        print("Please enter a valid integer for the year.")
