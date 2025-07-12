import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from library import LibraryDB, Book
class LibraryApp:
    def __init__(self, root):
        self.db = LibraryDB()
        self.root = root
        self.root.title("Библиотека")

        self.tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Year", text="Год")
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Добавить книгу", command=self.add_book).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Удалить книгу", command=self.delete_book).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Обновить книгу", command=self.update_book).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Поиск по автору", command=self.search_author).pack(side=tk.LEFT, padx=5)

        self.refresh_tree()

    def refresh_tree(self, books=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        books = books if books is not None else self.db.get_all_books()
        for book in books:
            self.tree.insert("", tk.END, values=(book.book_id, book.title, book.author, book.year))

    def add_book(self):
        title = simpledialog.askstring("Название", "Введите название книги:")
        author = simpledialog.askstring("Автор", "Введите автора книги:")
        year = simpledialog.askinteger("Год", "Введите год выпуска:")
        if title and author and year:
            self.db.add_book(Book(title, author, year))
            self.refresh_tree()

    def delete_book(self):
        selected = self.tree.selection()
        if selected:
            book_id = self.tree.item(selected[0])['values'][0]
            self.db.delete_book(book_id)
            self.refresh_tree()

    def update_book(self):
        selected = self.tree.selection()
        if selected:
            book_id = self.tree.item(selected[0])['values'][0]
            title = simpledialog.askstring("Новое название", "Введите новое название (или оставьте пустым):")
            author = simpledialog.askstring("Новый автор", "Введите нового автора (или оставьте пустым):")
            year = simpledialog.askinteger("Новый год", "Введите новый год (или оставьте пустым):")
            self.db.update_book(book_id, title, author, year)
            self.refresh_tree()

    def search_author(self):
        author = simpledialog.askstring("Поиск", "Введите имя автора:")
        if author:
            books = self.db.find_books_by_author(author)
            self.refresh_tree(books)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
