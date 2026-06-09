import random

def roll_dice():
    print("Rolling the dice...")
    result = random.randint(1, 6)
    print(f"The value is: {result}")

if __name__ == "__main__":
    while True:
        roll_dice()
        roll_again = input("Roll again? (y/n): ").lower()
        if roll_again != 'y':
            print("Thanks for playing!")
            break
