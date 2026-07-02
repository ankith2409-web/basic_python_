def is_palindrome(text):
    """Check if the given text is a palindrome."""
    # Clean the string: remove spaces and convert to lowercase
    cleaned_text = "".join(char.lower() for char in text if char.isalnum())
    # Check if string is equal to its reverse
    return cleaned_text == cleaned_text[::-1]

if __name__ == "__main__":
    user_input = input("Enter a string to check if it's a palindrome: ")
    if is_palindrome(user_input):
        print(f"'{user_input}' is a palindrome!")
    else:
        print(f"'{user_input}' is not a palindrome.")
