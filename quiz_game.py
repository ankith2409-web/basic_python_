def ask_question(question, options, correct_option):
    print(f"\n{question}")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    
    while True:
        try:
            answer = int(input("Enter your answer (1-4): "))
            if 1 <= answer <= len(options):
                if answer == correct_option:
                    print("Correct!")
                    return True
                else:
                    print(f"Wrong! The correct answer was: {options[correct_option - 1]}")
                    return False
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    print("--- General Knowledge Quiz ---")
    score = 0
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "correct": 3
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Mars", "Jupiter", "Venus", "Saturn"],
            "correct": 1
        },
        {
            "question": "Who wrote 'Hamlet'?",
            "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"],
            "correct": 2
        },
        {
            "question": "What is the largest ocean on Earth?",
            "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
            "correct": 4
        }
    ]

    for q in questions:
        if ask_question(q["question"], q["options"], q["correct"]):
            score += 1

    print(f"\nQuiz Finished! Your total score is {score}/{len(questions)}.")

if __name__ == "__main__":
    main()
