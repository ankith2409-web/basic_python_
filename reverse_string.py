def reverse_a_string(text):
    return text[::-1]

if __name__ == "__main__":
    user_input = input("Enter a string to reverse: ")
    reversed_string = reverse_a_string(user_input)
    print(f"Original: {user_input}")
    print(f"Reversed: {reversed_string}")
