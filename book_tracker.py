import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

DATA_FILE = 'books.json'

def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_books(books):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

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
    books.append(book)
 
