def caesar_cipher(text, shift, mode='encrypt'):
    """
    Encrypts or decrypts text using the Caesar Cipher algorithm.
    """
    result = []
    # If decrypting, we shift in the opposite direction
    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char.isalpha():
            # Determine ASCII base (uppercase vs lowercase)
            start = ord('A') if char.isupper() else ord('a')
            # Shift the character and wrap around the alphabet (26 letters)
            new_char = chr(start + (ord(char) - start + shift) % 26)
            result.append(new_char)
        else:
            # Leave non-alphabetical characters as they are
            result.append(char)

    return "".join(result)

def main():
    print("=== Caesar Cipher Encryption/Decryption ===")
    message = input("Enter your message: ")
    try:
        shift_key = int(input("Enter shift key (integer, e.g. 3): "))
    except ValueError:
        print("Invalid key! Shift key must be an integer. Using default shift of 3.")
        shift_key = 3

    encrypted = caesar_cipher(message, shift_key, 'encrypt')
    decrypted = caesar_cipher(encrypted, shift_key, 'decrypt')

    print(f"\nOriginal:  {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    main()
