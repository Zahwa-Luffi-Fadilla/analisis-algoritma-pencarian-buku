import csv
import time
import os


CSV_FILE = "google_books_dataset.csv"


class Buku:
    def __init__(self, book_id, title, author, category):
        self.book_id = str(book_id)
        self.title = str(title)
        self.author = str(author)
        self.category = str(category)


def ambil_kolom(row, pilihan):
    # Mencari nama kolom tanpa membedakan huruf besar/kecil.
    kolom = {k.strip().lower(): k for k in row.keys()}

    for nama in pilihan:
        if nama.lower() in kolom:
            return row[kolom[nama.lower()]]

    return ""


def baca_dataset(nama_file):
    if not os.path.exists(nama_file):
        raise FileNotFoundError(
            f"File {nama_file} tidak ditemukan. "
            "Letakkan dataset CSV di folder program."
        )

    books = []

    with open(
        nama_file, "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Dataset tidak memiliki header.")

        for row in reader:
            title = ambil_kolom(
                row, ["title", "book_title", "name"]
            )

            if not title.strip():
                continue

            book = Buku(
                ambil_kolom(row, ["book_id", "id", "isbn"]),
                title.strip(),
                ambil_kolom(row, ["author", "authors", "writer"]),
                ambil_kolom(
                    row, ["category", "genre", "categories"]
                ),
            )
            books.append(book)

    if not books:
        raise ValueError(
            "Tidak ada data buku yang valid. "
            "Periksa nama kolom pada dataset."
        )

    return books


def linear_search(books, keyword):
    comparisons = 0
    keyword = keyword.strip().casefold()

    for buku in books:
        comparisons += 1

        if buku.title.strip().casefold() == keyword:
            return buku, comparisons

    return None, comparisons


def binary_search(books, keyword):
    left = 0
    right = len(books) - 1
    comparisons = 0
    keyword = keyword.strip().casefold()

    while left <= right:
        mid = (left + right) // 2
        title = books[mid].title.strip().casefold()

        comparisons += 1
        if title == keyword:
            return books[mid], comparisons

        comparisons += 1
        if title < keyword:
            left = mid + 1
        else:
            right = mid - 1

    return None, comparisons


def ukur_waktu(fungsi, books, keyword, pengulangan=5):
    total = 0
    hasil = None
    perbandingan = 0

    for _ in range(pengulangan):
        mulai = time.perf_counter()
        hasil, perbandingan = fungsi(books, keyword)
        selesai = time.perf_counter()
        total += selesai - mulai

    return hasil, perbandingan, total / pengulangan


def tampilkan_buku(buku):
    if buku is None:
        print("Buku tidak ditemukan.")
        return

    print("ID Buku :", buku.book_id)
    print("Judul   :", buku.title)
    print("Penulis :", buku.author)
    print("Kategori:", buku.category)


def pengujian(books, n):
    # Ambil n buku, lalu urutkan berdasarkan judul.
    data = sorted(
        books[:n],
        key=lambda b: b.title.strip().casefold()
    )

    awal = data[0].title
    tengah = data[len(data) // 2].title
    akhir = data[-1].title
    tidak_ada = "JUDUL_TIDAK_ADA_987654321"

    skenario = [
        ("Posisi awal", awal),
        ("Posisi tengah", tengah),
        ("Posisi akhir", akhir),
        ("Tidak ditemukan", tidak_ada),
    ]

    print(f"\n{'=' * 70}")
    print(f"PENGUJIAN DENGAN n = {n}")
    print(f"{'=' * 70}")
    print(
        f"{'Algoritma':<16} {'Skenario':<20} "
        f"{'Perbandingan':>14} {'Waktu (detik)':>16}"
    )

    for nama, keyword in skenario:
        for nama_algoritma, fungsi in [
            ("Linear Search", linear_search),
            ("Binary Search", binary_search),
        ]:
            _, comparisons, elapsed = ukur_waktu(
                fungsi, data, keyword
            )

            print(
                f"{nama_algoritma:<16} {nama:<20} "
                f"{comparisons:>14} {elapsed:>16.8f}"
            )


def main():
    try:
        books = baca_dataset(CSV_FILE)

        print("Jumlah buku valid:", len(books))

        # Contoh pencarian interaktif.
        keyword = input(
            "\nMasukkan judul buku yang ingin dicari: "
        )

        # Binary Search memerlukan data terurut.
        books_sorted = sorted(
            books,
            key=lambda b: b.title.strip().casefold()
        )

        print("\n=== LINEAR SEARCH ===")
        hasil, comparisons, elapsed = ukur_waktu(
            linear_search, books, keyword
        )
        tampilkan_buku(hasil)
        print("Perbandingan:", comparisons)
        print("Waktu rata-rata:", elapsed, "detik")

        print("\n=== BINARY SEARCH ===")
        hasil, comparisons, elapsed = ukur_waktu(
            binary_search, books_sorted, keyword
        )
        tampilkan_buku(hasil)
        print("Perbandingan:", comparisons)
        print("Waktu rata-rata:", elapsed, "detik")

        # Pengujian untuk ukuran input yang diminta.
        for n in [100, 1000, 10000]:
            if len(books) >= n:
                pengujian(books, n)
            else:
                print(
                    f"\nPengujian n={n} dilewati: "
                    f"dataset hanya memiliki {len(books)} buku."
                )

    except (FileNotFoundError, ValueError, OSError) as error:
        print("Terjadi kesalahan:", error)


if __name__ == "__main__":
    main()