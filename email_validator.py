import re

def is_valid_email(email):
    """
    Validates an email address using a regular expression.
    """
    # Standard email validation regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    return False

def main():
    print("=== Simple Email Validator ===")
    test_emails = [
        "john.doe@example.com",
        "invalid-email.com",
        "alice@corp.co.uk",
        "bob@domain",
        "charlie.123@sub.domain.org"
    ]

    print("Testing predefined emails:")
    for email in test_emails:
        status = "Valid" if is_valid_email(email) else "Invalid"
        print(f" - {email}: {status}")

    print("\nTry it yourself!")
    user_email = input("Enter an email address to validate: ").strip()
    if is_valid_email(user_email):
        print(f"'{user_email}' is a VALID email address.")
    else:
        print(f"'{user_email}' is an INVALID email address.")

if __name__ == "__main__":
    main()
