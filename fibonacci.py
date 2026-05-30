def generate_fibonacci(n):
    """Generate the Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    while len(sequence) < n:
        next_val = sequence[-1] + sequence[-2]
        sequence.append(next_val)
    return sequence

if __name__ == "__main__":
    try:
        terms = int(input("Enter the number of terms for the Fibonacci sequence: "))
        result = generate_fibonacci(terms)
        print(f"Fibonacci sequence up to {terms} terms: {result}")
    except ValueError:
        print("Please enter a valid integer.")
