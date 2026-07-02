import random

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts}. Enter your guess: "))
            attempts += 1
            
            if guess < 1 or guess > 100:
                print("Please enter a number within the range of 1 to 100.")
                attempts -= 1  # Don't count invalid range inputs as attempts
                continue
                
            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts!")
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
    if attempts >= max_attempts and guess != secret_number:
        print(f"\nGame Over! The secret number was {secret_number}.")

if __name__ == "__main__":
    number_guessing_game()
