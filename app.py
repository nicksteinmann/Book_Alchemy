from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev-key"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    sort_by = request.args.get("sort", "title")

    if sort_by == "author":
        books = Book.query.join(Author).order_by(Author.name, Book.title).all()
    else:
        books = Book.query.order_by(Book.title).all()

    return render_template("home.html", books=books, sort_by=sort_by)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birth_date_raw = request.form.get("birth_date", "").strip()
        date_of_death_raw = request.form.get("date_of_death", "").strip()

        if not name or not birth_date_raw:
            flash("Bitte Name und Geburtsdatum ausfüllen.")
            return render_template("add_author.html")

        birth_date = datetime.strptime(birth_date_raw, "%Y-%m-%d").date()
        date_of_death = (
            datetime.strptime(date_of_death_raw, "%Y-%m-%d").date()
            if date_of_death_raw
            else None
        )

        new_author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(new_author)
        db.session.commit()

        flash("Autor erfolgreich hinzugefügt.")
        return redirect(url_for("home"))

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    authors = Author.query.order_by(Author.name).all()

    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        publication_year_raw = request.form.get("publication_year", "").strip()
        author_id_raw = request.form.get("author_id", "").strip()

        if not isbn or not title or not publication_year_raw or not author_id_raw:
            flash("Bitte alle Pflichtfelder ausfüllen.")
            return render_template("add_book.html", authors=authors)

        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=int(publication_year_raw),
            author_id=int(author_id_raw)
        )

        db.session.add(new_book)
        db.session.commit()

        flash("Buch erfolgreich hinzugefügt.")
        return redirect(url_for("home"))

    return render_template("add_book.html", authors=authors)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
