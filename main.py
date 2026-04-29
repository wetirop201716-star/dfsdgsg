import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_data()

        # Создаём виджеты
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название книги:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.root, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = tk.Entry(self.root, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, sticky="w")
        self.genre_entry = tk.Entry(self.root, width=40)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Количество страниц:").grid(row=3, column=0, sticky="w")
        self.pages_entry = tk.Entry(self.root, width=40)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, sticky="w")
        self.genre_filter = ttk.Combobox(self.root, values=["Все", "Роман", "Фантастика", "Детектив", "Поэзия"])
        self.genre_filter.set("Все")
        self.genre_filter.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.root, text="Фильтр по страницам:").grid(row=6, column=0, sticky="w")
        self.pages_filter = ttk.Combobox(self.root, values=["Все", ">200", ">300", ">500"])
        self.pages_filter.set("Все")
        self.pages_filter.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=0, pady=5)
        tk.Button(self.root, text="Сбросить фильтр", command=self.reset_filter).grid(row=7, column=1, pady=5)

        # Таблица
        columns = ("Название", "Автор", "Жанр", "Страниц")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Кнопки сохранения/загрузки
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=9, column=0, pady=5)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_data).grid(row=9, column=1, pady=5)

    def validate_input(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return False
        try:
            pages = int(pages)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return False
        return True, title, author, genre, pages

    def add_book(self):
        validation_result = self.validate_input()
        if not validation_result:
            return

        is_valid, title, author, genre, pages = validation_result
        book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(book)
        self.update_table()
        # Очищаем поля ввода
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in self.books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_filter = self.genre_filter.get()
        pages_filter = self.pages_filter.get()

        filtered_books = self.books
        if genre_filter != "Все":
            filtered_books = [b for b in filtered_books if b["genre"]] == genre_filter
        if pages_filter != "Все":
            min_pages = int(pages_filter[1:])
            filtered_books = [b for b in filtered_books if b["pages"]] >= min_pages

        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in filtered_books:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

    def reset_filter(self):
        self.update_table()

    def save_data(self):
        with open("books_data.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в books_data.json")

    def load_data(self):
        if os.path.exists("books_data.json"):
            try:
                with open("books_data.json", "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.update_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()

