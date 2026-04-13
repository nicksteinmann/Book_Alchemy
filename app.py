from flask import Flask, render_template, request, redirect, url_for, flash
import os
from data_models import db, Author, Book
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev-key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Displays all books with optional search and sorting."""
    sort_by = request.args.get("sort", "title")
    search = request.args.get("search", "").strip()

    query = Book.query.join(Author)

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    if sort_by == "author":
        books = query.order_by(Author.name, Book.title).all()
    else:
        books = query.order_by(Book.title).all()

    return render_template("home.html", books=books, sort_by=sort_by, search=search)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Handles adding a new author to the database."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birth_date_raw = request.form.get("birth_date", "").strip()
        date_of_death_raw = request.form.get("date_of_death", "").strip()

        if not name or not birth_date_raw:
            flash("Bitte Name und Geburtsdatum ausfüllen.")
            return render_template("add_author.html")

        try:
            birth_date = datetime.strptime(birth_date_raw, "%Y-%m-%d").date()
        except ValueError:
            flash("Ungültiges Geburtsdatum.")
            return render_template("add_author.html")

        if date_of_death_raw:
            try:
                date_of_death = datetime.strptime(date_of_death_raw, "%Y-%m-%d").date()
            except ValueError:
                flash("Ungültiges Sterbedatum.")
                return render_template("add_author.html")
        else:
            date_of_death = None

        existing_author = Author.query.filter_by(
            name=name,
            birth_date=birth_date
        ).first()

        if existing_author:
            flash("Dieser Autor existiert bereits.")
            return render_template("add_author.html")

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        try:
            db.session.add(new_author)
            db.session.commit()
            flash("Autor erfolgreich hinzugefügt.")
            return redirect(url_for("home"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("Fehler beim Speichern des Autors.")
            return render_template("add_author.html")

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Handles adding a new book linked to an author."""
    authors = Author.query.order_by(Author.name).all()

    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        publication_year_raw = request.form.get("publication_year", "").strip()
        author_id_raw = request.form.get("author_id", "").strip()

        if not isbn or not title or not publication_year_raw or not author_id_raw:
            flash("Bitte alle Pflichtfelder ausfüllen.")
            return render_template("add_book.html", authors=authors)

        try:
            publication_year = int(publication_year_raw)
            author_id = int(author_id_raw)
        except ValueError:
            flash("Publikationsjahr und Autor müssen gültige Werte sein.")
            return render_template("add_book.html", authors=authors)

        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id
        )

        try:
            db.session.add(new_book)
            db.session.commit()
            flash("Buch erfolgreich hinzugefügt.")
            return redirect(url_for("home"))
        except SQLAlchemyError:
            db.session.rollback()
            flash("Fehler beim Speichern des Buches.")
            return render_template("add_book.html", authors=authors)

    return render_template("add_book.html", authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """Deletes a book from the database."""
    book = Book.query.get_or_404(book_id)

    try:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully.")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Error deleting book.")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
