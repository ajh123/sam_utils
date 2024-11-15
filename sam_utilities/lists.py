from typing import List, Any
from sam_utilities import validated_input


def dual_sort(list1: List[Any], list2: List[Any] | None):
    """
    Sorts `list1` in ascending order while applying the same reordering to `list2`.

    This function performs a parallel bubble sort, rearranging elements in `list1` 
    such that they are sorted in ascending order. The elements in `list2` are 
    reordered in the same way as `list1` to maintain their original pairing.

    `list2` is optional so you can perform a single bubble sort.

    Parameters:
        list1 (List[Any]): The primary list of elements to sort in ascending order.
        list2 (List[Any] | None): The secondary list to reorder in correspondence with `list1`.

    Raises:
        ValueError: If `list1` and `list2` are not of the same length.

    Example:
    ```python
    list1 = [7, 2, 5, 10]
    list2 = ['a', 'b', 'c', 'd']
    dual_sort(list1, list2)
    print(list1)  # Output: [2, 5, 7, 10]
    print(list2)  # Output: ['b', 'c', 'a', 'd']
    ```
    """
    if list2 is not None:
        if len(list1) > len(list2):
            raise ValueError("Legnth of `list1` is greater then length of `list2`.")
    
    # fully_sorted = False

    # while not fully_sorted:
    #     last_index = 0
    #     for i in range(0, len(list1)):
    #         if list1[i] < list1[last_index]:
    #             swap(list1, last_index, i)
    #             swap(list2, last_index, i)
    #         last_index = i
        
    #     last_index = 0
    #     for i in range(0, len(list1)):
    #         if list1[i] < list1[last_index]:
    #             fully_sorted = False
    #         else:
    #             fully_sorted = True
    #         last_index = i
    l = len(list1)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if list1[j] > list1[j+1]:  
                swap(list1, j, j+1)
                if list2 is not None:
                    swap(list2, j, j+1)


def swap(in_list, start_index: int, end_index: int):
    ele1 = in_list[start_index]
    ele2 = in_list[end_index]
    in_list[start_index] = ele2
    in_list[end_index] = ele1


def linear_search(haystack: List[Any], needle: Any) -> int | None:
    for i in range(0, len(haystack)):
        if needle in haystack[i]:
            return i
    return None


def binary_search(haystack: List[Any], needle: Any) -> int | None:
    start = 0
    end = len(haystack)
    while start < end:
        mid = (start + end) // 2
        if haystack[mid] == needle:
            return mid
        elif mid < needle:
            start = mid + 1
        else:
            end = mid - 1
    if start > end:
        return None
    

def merge_sort(numbers: List[int]) -> List[int]:
    width = 1
    n = len(numbers)
    while width < n:
        left = 0
        while left < n:
            right = min(left + width * 2 - 1, n - 1)
            middle = min(left + width - 1, n - 1)
            numbers = merge(numbers, left, middle, right)
            left = left + width * 2
        width = width * 2
    return numbers

def merge(numbers: List[int], left: int, middle: int, right: int) -> List[int]:
    lengthLeft = middle - left + 1
    lengthRight = right - middle
    l = [0 for _ in range(0, lengthLeft)]
    r = [0 for _ in range(0, lengthRight)]
    for i in range(0, lengthLeft):
        l[i] = numbers[left + i]
    for i in range(0, lengthRight):
        r[i] = numbers[middle + i + 1]
    indexLeft = 0
    indexRight = 0
    indexMain = left
    while indexLeft < lengthLeft and indexRight < lengthRight:
        if l[indexLeft] <= r[indexRight]:
            numbers[indexMain] = l[indexLeft]
            indexLeft = indexLeft + 1
        else:
            numbers[indexMain] = r[indexRight]
            indexRight = indexRight + 1
        indexMain = indexMain + 1
    while indexLeft < lengthLeft:
        numbers[indexMain] = l[indexLeft]
        indexMain = indexMain + 1
        indexLeft = indexLeft + 1
    while indexRight < lengthRight:
        numbers[indexMain] = r[indexRight]
        indexMain = indexMain + 1
        indexRight = indexRight + 1
    return numbers

if __name__ == "__main__":
    # # Test dual sort
    # thing = [7, 2, 5, 10, 100, -30]
    # thing2 = ["A", "B", "C", "D", "E", "F"]
    # dual_sort(thing, thing2)
    # print(thing)
    # print(thing2)
    
    # # Test linear seach
    # print(linear_search(thing2, "D"))
    
    # # Test binary search
    # thing3 = list(range(0, 100))
    # print(thing3)
    # num = validated_input(int, "Enter a number you want to find")
    # res = binary_search(thing3, num)
    # if res is None:
    #     print("Not in list")
    # else:
    #     print(f"{num} found at poistion {res}")

    # Test merge sort
    import random
    thing4 = list(range(0, 100))
    random.shuffle(thing4)
    thing4 = merge_sort(thing4)
    print(thing4)