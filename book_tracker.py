import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("700x500")

        # Создание виджетов
        self.create_widgets()
        self.load_books()
        self.update_treeview()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.pages_entry = tk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("title", "author", "genre", "pages"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("genre", width=100)
        self.tree.column("pages", width=80)
        self.tree.grid(row=5, column=0, columnspan=2, sticky="nsew")

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.filter_genre = tk.Entry(self.root, width=30)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по страницам (>):").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.filter_pages = tk.Entry(self.root, width=30)
        self.filter_pages.grid(row=7, column=1, padx=5, pady=5)

        self.filter_btn = tk.Button(self.root, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=8, column=0, columnspan=2, pady=10)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(book)
        self.save_books()
        self.update_treeview()

    def load_books(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
                for book in self.books:
                    book['pages'] = int(book['pages'])
        else:
            self.books = []

    def save_books(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in self.books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        try:
            pages_filter = int(self.filter_pages.get().strip())
        except:
            pages_filter = 0

        filtered_books = []

        for book in self.books:
            match_genre = genre_filter == "" or genre_filter in book["genre"].lower()
            match_pages = pages_filter == 0 or book["pages"] > pages_filter

            if match_genre and match_pages:
                filtered_books.append(book)

        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in filtered_books:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
