def is_anagram(str1, str2):
    """
    Checks if two strings are anagrams of each other.
    """
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    return sorted(str1) == sorted(str2)

if __name__ == "__main__":
    word1 = input("Enter first word: ")
    word2 = input("Enter second word: ")
    if is_anagram(word1, word2):
        print(f"'{word1}' and '{word2}' are anagrams!")
    else:
        print(f"'{word1}' and '{word2}' are not anagrams.")
