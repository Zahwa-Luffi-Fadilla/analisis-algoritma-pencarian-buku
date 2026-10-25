class HasilPencarian:
    def __init__(
        self, found, data, comparisons, elapsed_time
    ):
        self.found = found
        self.data = data
        self.comparisons = comparisons
        self.elapsed_time = elapsed_time

    def tampilkan(self):
        print("Ditemukan       :", self.found)
        print("Jumlah hasil    :", len(self.data))
        print("Perbandingan    :", self.comparisons)
        print("Waktu eksekusi  :", self.elapsed_time, "detik")