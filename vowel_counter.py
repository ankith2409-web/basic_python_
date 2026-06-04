def count_vowels(text):
    """
    Counts the number of vowels in a given string.
    """
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

if __name__ == "__main__":
    user_text = input("Enter a string: ")
    vowel_count = count_vowels(user_text)
    print(f"The number of vowels in the string is: {vowel_count}")
