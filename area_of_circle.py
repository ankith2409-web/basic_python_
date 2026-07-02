import math

def calculate_area(radius):
    return math.pi * (radius ** 2)

if __name__ == "__main__":
    try:
        radius = float(input("Enter the radius of the circle: "))
        if radius < 0:
            print("Radius cannot be negative.")
        else:
            area = calculate_area(radius)
            print(f"The area of the circle with radius {radius} is {area:.2f}")
    except ValueError:
        print("Please enter a valid number.")
