import string

def get_word_frequencies(text):
    """
    Counts the frequency of each word in a given text.
    """
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = text.split()
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies

if __name__ == "__main__":
    user_text = input("Enter some text: ")
    freq = get_word_frequencies(user_text)
    print("Word Frequencies:")
    for word, count in freq.items():
        print(f"{word}: {count}")
