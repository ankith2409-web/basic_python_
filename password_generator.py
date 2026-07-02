import random
import string

def generate_password(length=12):
    """
    Generates a strong random password of the specified length.
    """
    if length < 4:
        return "Password length should be at least 4."
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

if __name__ == "__main__":
    try:
        length = int(input("Enter password length (default 12): ") or 12)
        print(f"Generated Password: {generate_password(length)}")
    except ValueError:
        print("Please enter a valid number.")
