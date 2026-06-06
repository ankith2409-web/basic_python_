def double_numbers(numbers):
    # Using list comprehension to double each number in the list
    return [num * 2 for num in numbers]

if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5]
    print(f"Original: {nums}")
    print(f"Doubled: {double_numbers(nums)}")
