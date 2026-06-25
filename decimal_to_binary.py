def decimal_to_binary_octal_hex(n):
    """
    Converts a decimal number into binary, octal, and hexadecimal representations.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Please enter a non-negative integer.")
        
    return {
        "binary": bin(n),
        "octal": oct(n),
        "hexadecimal": hex(n)
    }

def main():
    print("=== Decimal Converter ===")
    try:
        num = int(input("Enter a non-negative decimal integer: "))
        results = decimal_to_binary_octal_hex(num)
        print(f"\nDecimal: {num}")
        print(f"Binary:      {results['binary']}")
        print(f"Octal:       {results['octal']}")
        print(f"Hexadecimal: {results['hexadecimal']}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
