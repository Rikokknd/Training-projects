def binary_search(input_array, value):
    """Returns index of the element that matches the search value.
    Returns -1 if element does not exist."""
    left, right = 0, len(input_array) - 1
    while left != right:
        middle = (right + left) // 2
        if input_array[middle] == value:
            return middle
        elif input_array[middle] > value:
            right = middle
        elif input_array[middle] < value:
            left = middle + 1
    return -1

test_list = [1,3,9,11,15,19,29]
test_val1 = 25
test_val2 = 15
print(binary_search(test_list, test_val1))
print(binary_search(test_list, test_val2))