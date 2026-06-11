def display_menu():
    print("\n--- To-Do List Manager ---")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Mark Task as Done")
    print("4. Remove Task")
    print("5. Exit")

def main():
    tasks = []
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            if not tasks:
                print("Your to-do list is empty!")
            else:
                print("\nYour Tasks:")
                for idx, task in enumerate(tasks, 1):
                    status = "[x]" if task['done'] else "[ ]"
                    print(f"{idx}. {status} {task['name']}")
        elif choice == '2':
            task_name = input("Enter task name: ")
            tasks.append({"name": task_name, "done": False})
            print(f"Task '{task_name}' added.")
        elif choice == '3':
            try:
                task_num = int(input("Enter task number to mark as done: "))
                if 1 <= task_num <= len(tasks):
                    tasks[task_num - 1]['done'] = True
                    print("Task marked as done.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            try:
                task_num = int(input("Enter task number to remove: "))
                if 1 <= task_num <= len(tasks):
                    removed = tasks.pop(task_num - 1)
                    print(f"Task '{removed['name']}' removed.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '5':
            print("Exiting To-Do List Manager. Have a productive day!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
