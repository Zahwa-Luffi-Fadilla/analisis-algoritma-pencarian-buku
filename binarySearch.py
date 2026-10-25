def binary_search(books, keyword):
    left = 0
    right = len(books) - 1
    comparisons = 0

    keyword = keyword.strip().casefold()

    while left <= right:
        mid = (left + right) // 2
        judul = books[mid].title.strip().casefold()

        comparisons += 1

        if judul == keyword:
            return books[mid], comparisons

        comparisons += 1

        if judul < keyword:
            left = mid + 1
        else:
            right = mid - 1

    return None, comparisons