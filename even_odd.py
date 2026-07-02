def check_even_odd(number):
    """
    Checks if a given number is even or odd.
    """
    if number % 2 == 0:
        return f"{number} is Even."
    else:
        return f"{number} is Odd."

if __name__ == "__main__":
    try:
        num = int(input("Enter a number: "))
        print(check_even_odd(num))
    except ValueError:
        print("Please enter a valid integer.")
