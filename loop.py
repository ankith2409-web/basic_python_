# Variables & Data Types
name = "Ankith"        # str
age = 20               # int
gpa = 8.5              # float
is_student = True      # bool
skills = ["Python", "React", "AI"]  # list

# Control Flow - if/elif/else
if gpa >= 9.0:
    grade = "Outstanding"
elif gpa >= 7.5:
    grade = "Excellent"
else:
    grade = "Good"

print(f"Name: {name}, Age: {age}, Grade: {grade}")

# for loop
print("Skills:")
for skill in skills:
    print(f"  - {skill}")

# while loop
count = 1
while count <= 3:
    print(f"Round {count}")
    count += 1
