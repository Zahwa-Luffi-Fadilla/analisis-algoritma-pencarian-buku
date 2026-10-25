class Buku:
    def __init__(self, book_id, title, author, category):
        self.book_id = str(book_id)
        self.title = str(title)
        self.author = str(author)
        self.category = str(category)

    def tampilkan(self):
        print("ID Buku :", self.book_id)
        print("Judul   :", self.title)
        print("Penulis :", self.author)
        print("Kategori:", self.category)