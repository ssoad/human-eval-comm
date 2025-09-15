def test_quick_sort():
    """Test quicksort function."""
    from solution import quick_sort

    # Test basic sorting
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    # Test empty array
    assert quick_sort([]) == []

    # Test single element
    assert quick_sort([42]) == [42]

    # Test already sorted
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    # Test reverse sorted
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_bubble_sort():
    """Test bubble sort function."""
    from solution import bubble_sort

    # Test basic sorting
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    bubble_sort(arr)
    assert arr == [1, 1, 2, 3, 4, 5, 6, 9]

    # Test empty array
    arr = []
    bubble_sort(arr)
    assert arr == []

    # Test single element
    arr = [42]
    bubble_sort(arr)
    assert arr == [42]
