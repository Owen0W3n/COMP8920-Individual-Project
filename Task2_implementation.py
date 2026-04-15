def heapify(arr, n, i):

    largest = i          # Assume root is largest
    left = 2 * i + 1     # Left child index
    right = 2 * i + 2    # Right child index

    # check if left child nodes is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child nodes exist and is greater than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    # re-heapify
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        # Recursively heapify the affected subtree
        heapify(arr, n, largest)


def heap_sort(arr):


    n = len(arr)

    # max-heaping
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


    for i in range(n - 1, 0, -1):
        # node swapping
        arr[i], arr[0] = arr[0], arr[i]

        # re-heapify
        heapify(arr, i, 0)



data = [1,5,4,6,19,90,22,35,5,67,69,34,19]

print("Original rank:", data)

heap_sort(data)

print("Sorted rank:", data)