def is_prime(n):
    """
    Checks if a given number is a prime number.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    try:
        num = int(input("Enter a number to check if it's prime: "))
        if is_prime(num):
            print(f"{num} is a Prime number.")
        else:
            print(f"{num} is not a Prime number.")
    except ValueError:
        print("Please enter a valid integer.")
