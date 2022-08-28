def quicksort(array):
    if len(array) == 1:
        return array
    else:
        pivot = array[0]
        storing = 0 # index of the next cell after pivot

        for i in range(1, len(array)): # running through all cells except pivot
            if pivot > array[i]: # every cell that is lesser than pivot 
                storing += 1 #  next found value will be swapped into the next closest cell
                array[i], array[storing] = array[storing], array[i] # swap found element with closest cell

        array[0], array[storing] = array[storing], array[0] # swap pivot with the last found lesser element
        if storing > 0: # if there are elements to the left of pivot
            array[:storing] = quicksort(array[:storing]) # try to sort them too
        if storing + 1 < len(array): # if the pivot is stored far enought from the end of list (at least one element to the right)
            array[storing + 1:] = quicksort(array[storing + 1:]) # try to sort them
        return array

test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14, 55]
test2 = [1, 0]
print(test)
print(quicksort(test))