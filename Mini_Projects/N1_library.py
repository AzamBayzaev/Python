# library.py

import sqlite3

class Book:
    def __init__(self, title, author, year, book_id=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f'"{self.title}" by {self.author} ({self.year})'

class LibraryDB:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._connect() as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL
            )
            '''
            conn.execute(query)

    def add_book(self, book):
        with self._connect() as conn:
            query = 'INSERT INTO books (title, author, year) VALUES (?, ?, ?)'
            cursor = conn.execute(query, (book.title, book.author, book.year))
            book.book_id = cursor.lastrowid
            return book.book_id

    def get_all_books(self):
        with self._connect() as conn:
            cursor = conn.execute('SELECT id, title, author, year FROM books')
            return [Book(row[1], row[2], row[3], row[0]) for row in cursor]

    def find_books_by_author(self, author):
        with self._connect() as conn:
            cursor = conn.execute('SELECT id, title, author, year FROM books WHERE LOWER(author) LIKE LOWER(?)',
                                  (f'%{author}%',))
            return [Book(row[1], row[2], row[3], row[0]) for row in cursor]

    def update_book(self, book_id, new_title=None, new_author=None, new_year=None):
        with self._connect() as conn:
            updates = []
            params = []
            if new_title:
                updates.append("title = ?")
                params.append(new_title)
            if new_author:
                updates.append("author = ?")
                params.append(new_author)
            if new_year:
                updates.append("year = ?")
                params.append(new_year)

            if not updates:
                return False

            params.append(book_id)
            query = f'UPDATE books SET {", ".join(updates)} WHERE id = ?'
            conn.execute(query, params)
            return True

    def delete_book(self, book_id):
        with self._connect() as conn:
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            return True
