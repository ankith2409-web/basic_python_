def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        # If target is smaller, ignore right half
        else:
            right = mid - 1
            
    # Target is not present in the array
    return -1

if __name__ == "__main__":
    sorted_arr = [2, 3, 4, 10, 40]
    x = 10
    result = binary_search(sorted_arr, x)
    if result != -1:
        print(f"Element {x} is present at index {result}")
    else:
        print(f"Element {x} is not present in array")
