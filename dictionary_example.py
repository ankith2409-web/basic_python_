def run_dictionary_example():
    # Creating a dictionary
    student = {
        "name": "Alice",
        "age": 20,
        "major": "Computer Science"
    }
    
    # Accessing values
    print(f"Student Name: {student['name']}")
    
    # Adding a new key-value pair
    student["grade"] = "A"
    
    # Iterating over the dictionary
    for key, value in student.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    run_dictionary_example()
