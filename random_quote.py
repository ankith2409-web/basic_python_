import random

def get_random_quote():
    quotes = [
        "Be yourself; everyone else is already taken. - Oscar Wilde",
        "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe. - Albert Einstein",
        "Be the change that you wish to see in the world. - Mahatma Gandhi",
        "If you tell the truth, you don't have to remember anything. - Mark Twain",
        "A room without books is like a body without a soul. - Marcus Tullius Cicero"
    ]
    return random.choice(quotes)

if __name__ == "__main__":
    print("Here is a random quote for you:")
    print("-" * 40)
    print(get_random_quote())
    print("-" * 40)
