def display_menu():
    print("\n--- Contact Book ---")
    print("1. Add a contact")
    print("2. View all contacts")
    print("3. Search for a contact")
    print("4. Exit")

def main():
    contacts = {}
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            contacts[name] = phone
            print(f"Contact '{name}' added successfully!")
        elif choice == '2':
            if not contacts:
                print("No contacts found.")
            else:
                print("\nContacts:")
                for name, phone in contacts.items():
                    print(f"- {name}: {phone}")
        elif choice == '3':
            name = input("Enter name to search: ")
            if name in contacts:
                print(f"Found: {name} - {contacts[name]}")
            else:
                print(f"Contact '{name}' not found.")
        elif choice == '4':
            print("Exiting Contact Book. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
