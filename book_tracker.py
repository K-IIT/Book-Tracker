import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Конфигурация ---
DATA_FILE = 'books.json'
MAX_TITLE_LEN = 100
MAX_AUTHOR_LEN = 100
MAX_GENRE_LEN = 50

# --- Работа с данными ---
def load_books():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except (json.JSONDecodeError, OSError) as e:
        messagebox.showerror("Ошибка файла", f"Не удалось загрузить данные: {e}")
        return []

def save_books(books):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
    except OSError as e:
        messagebox.showerror("Ошибка файла", f"Не удалось сохранить данные: {e}")

# --- Логика приложения ---
class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("800x600")
        self.books = load_books()

        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        # --- Поля ввода ---
        frame_input = tk.LabelFrame(self.root, text="Добавить книгу", padx=10, pady=10)
        frame_input.pack(pady=10, fill='x')

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky='e')
        self.entry_title = tk.Entry(frame_input, width=40)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Автор:").grid(row=1, column=0, sticky='e')
        self.entry_author = tk.Entry(frame_input, width=40)
        self.entry_author.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Жанр:").grid(row=2, column=0, sticky='e')
        self.entry_genre = tk.Entry(frame_input, width=40)
        self.entry_genre.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Страниц:").grid(row=3, column=0, sticky='e')
        self.entry_pages = tk.Entry(frame_input, width=10)
        self.entry_pages.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        tk.Button(frame_input, text="Добавить книгу", command=self.add_book).grid(
            row=4, column=0, columnspan=2, pady=10)

        # --- Фильтрация ---
        frame_filter = tk.LabelFrame(self.root, text="Фильтр", padx=10, pady=10)
        frame_filter.pack(pady=10, fill='x')

        tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, sticky='e')
        self.filter_genre = tk.Entry(frame_filter, width=30)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filter, text="Мин. страниц:").grid(row=1, column=0, sticky='e')
        self.filter_pages = tk.Entry(frame_filter, width=10)
        self.filter_pages.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter).grid(
            row=2, column=0, columnspan=2, pady=10)

        # --- Таблица книг ---
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, minwidth=0, width=180)
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

    def add_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        genre = self.entry_genre.get().strip()
        pages_str = self.entry_pages.get().strip()

        # Валидация
        if not (title and author and genre and pages_str):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if len(title) > MAX_TITLE_LEN or len(author) > MAX_AUTHOR_LEN or len(genre) > MAX_GENRE_LEN:
            messagebox.showerror("Ошибка", "Превышена максимальная длина строки.")
            return

        if not pages_str.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть целым числом.")
            return

        pages = int(pages_str)
        if pages <= 0:
            messagebox.showerror("Ошибка", "Количество страниц должно быть больше 0.")
            return

        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        save_books(self.books)
        self.update_treeview()
        
    def apply_filter(self):
        genre = self.filter_genre.get().strip().lower()
        pages_str = self.filter_pages.get().strip()
        
        min_pages = None
        if pages_str:
            if not pages_str.isdigit():
                messagebox.showerror("Ошибка", "Мин. страниц — целое число.")
                return
            min_pages = int(pages_str)
        
        filtered_books = []
        for book in self.books:
            if genre and book["genre"].lower() != genre:
                continue
            if min_pages is not None and book["pages"] < min_pages:
                continue
            filtered_books.append(book)
        
        self.display_books(filtered_books)
    
    def display_books(self, books_to_show):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for book in books_to_show:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))
    
    def update_treeview(self):
        self.display_books(self.books)

# --- Точка входа ---
if __name__ == '__main__':
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
