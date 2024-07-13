from flask import Flask, render_template, Response, request
import db

app = Flask(__name__, template_folder="./templates", static_folder="./static")
data = db.DB()


@app.route("/")
def main_page():
    """Route for the main page of All Books"""
    all_books = data.get_all_books()
    return render_template("index.html", data=all_books)


@app.route("/authors")
def authors():
    """Routing for the Authors page"""
    all_authors = data.get_all_authors()
    return render_template("authors.html", data=all_authors)


@app.route("/delete_author", methods=["POST"])
def delete_author():
    """Endpoint for the process of deleting author with books"""
    id_data = request.get_json()
    author_id = id_data.get("author_name")
    ok = data.delete_author_and_books(author_id)
    if ok:
        return Response(status=200)
    else:
        return Response(status=500)


@app.route("/add_author", methods=["POST"])
def add_author():
    """Endpoint for adding author(recieves form submission)"""
    name = request.form["name"]
    ok = data.add_author(name)
    if ok:
        return render_template(
            "form_submit_screen.html", result="Author added successfully"
        )
    else:
        return render_template("form_submit_screen.html", result=str(ok))


@app.route("/download")
def download():
    """Endpoint that returns returns .csv file representing database"""
    fl = data.export_books()
    return Response(
        fl,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=books.csv"},
    )


@app.route("/add_book", methods=["POST"])
def add_book():
    """Endpoint for adding books(recieves form submission)"""
    title = request.form["title"]
    desc = request.form["description"]
    author = request.form["author"]
    ok = data.add_book(title, desc, author)
    if ok:
        return render_template(
            "form_submit_screen.html", result="Book added successfully"
        )
    else:
        return render_template("form_submit_screen.html", result=str(ok))


@app.route("/delete_book", methods=["POST"])
def delete_book():
    """Endpoint for deleting bboks"""
    id_data = request.get_json()
    book_id = id_data.get("book_id")
    ok = data.delete_book(book_id)
    if ok:
        return Response(status=200)
    else:
        return Response(status=500)


@app.route("/edit_book", methods=["POST"])
def edit_book():
    """Endpoint for editinf books(recieves form submission)"""
    id = request.form["id"]
    title = request.form["title"]
    desc = request.form["description"]
    author = request.form["author"]
    ok = data.edit_book_by_id(id, title, desc, author)
    if ok:
        return render_template("form_submit_screen.html", result="Book added edited")
    else:
        return render_template("form_submit_screen.html", result=str(ok))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
