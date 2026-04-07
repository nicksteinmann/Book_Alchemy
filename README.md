# 📚 Book Alchemy – Digital Library

A simple Flask web application to manage a personal book library with authors, books, search, sorting and deletion.

---

## 🚀 Features

- Add authors
- Add books linked to authors
- Display books with cover images (via ISBN)
- Sort books by title or author
- Search books by keyword
- Delete books directly from the homepage

---

## 🛠️ Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Jinja2
- HTML & CSS

---

## 📂 Project Structure

Book_Alchemy/
│
├── app.py
├── data_models.py
├── data/
│ └── library.sqlite
├── static/
│ └── style.css
├── templates/
│ ├── home.html
│ ├── add_author.html
│ └── add_book.html
└── README.md

---

## ⚙️ Installation & Setup

1. Clone repository:
   git clone https://github.com/nicksteinmann/Book_Alchemy.git
   cd Book_Alchemy

2. Install dependencies:
   pip install flask flask_sqlalchemy

3. Run application:
   python app.py

4. Open in browser:
   http://127.0.0.1:5002

---

## 📖 Usage

- Create authors first
- Add books and assign them to authors
- Use search to find books by title
- Sort books using dropdown
- Delete books directly from homepage

---

## 🧠 How it works

- Books are linked to authors via foreign key
- Covers are loaded dynamically using ISBN:
  https://covers.openlibrary.org/b/isbn/{ISBN}-M.jpg
- Search uses SQL LIKE via SQLAlchemy
- Sorting uses query parameters (?sort=title / ?sort=author)

---

## 📌 Notes

- ISBN is only used for cover images
- Authors are NOT automatically deleted
- SQLite is used as local database

---

## 👤 Author

Nick Steinmann