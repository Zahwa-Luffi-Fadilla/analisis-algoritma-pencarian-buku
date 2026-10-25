def linear_search(books, keyword):
    hasil = []
    comparisons = 0

    keyword = keyword.strip().casefold()

    for buku in books:
        comparisons += 1

        if buku.title.strip().casefold() == keyword:
            hasil.append(buku)

    return hasil, comparisons