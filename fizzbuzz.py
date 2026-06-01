def fizzbuzz(n):
    """
    Prints numbers from 1 to n. 
    But for multiples of 3, print 'Fizz' instead of the number, 
    and for the multiples of 5, print 'Buzz'. 
    For numbers which are multiples of both 3 and 5, print 'FizzBuzz'.
    """
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

if __name__ == "__main__":
    try:
        limit = int(input("Enter a number for FizzBuzz: "))
        fizzbuzz(limit)
    except ValueError:
        print("Please enter a valid integer.")
