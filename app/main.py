import baza
import test_data

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

test_data.add_test_data()

@app.route("/")
def home():
    """
    """

    return render_template("home.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    """
    """

    if request.method == "POST":
        item = request.form.get("search")
        b = baza.Baza()
        return render_template("search.html", text=b.search(item))
    return render_template("search.html", text="Run query")


@app.route("/order", methods=["POST", "GET"])
def order():
    """
    """

    if request.method == "POST":
        bookid = request.form.get("bookid")
        params = {}
        params['name'] = request.form.get("name")
        params['surname'] = request.form.get("surname")

        b = baza.Baza()
        b.add_request(bookid, params)
        return render_template("order.html",
                               text="bookid:{} name:{} surname:{}".format(bookid, params['name'], params['surname']))
    return render_template("order.html")


@app.route("/admin")
def admin():
    """
    """

    return render_template("admin.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    """
    """

    if request.method == "POST":
        params = {}
        params["title"] = request.form.get("title")
        params["author"] = request.form.get("author")
        params["publisher"] = request.form.get("publisher")
        params["owner"] = request.form.get("book_owner")
        params["isbn"] = request.form.get("isbn")
        params["pages"] = request.form.get("pages")
        params["category"] = request.form.get("category")
        params["description"] = request.form.get("description")
        params["state"] = request.form.get("state")

        b = baza.Baza()
        b.add_book(params)

        return render_template("add.html", text="New book was added to database")
    return render_template("add.html")


@app.route("/update", methods=["POST", "GET"])
def update():
    """
    """

    b = baza.Baza()

    if request.method == "POST":
        params = {}
        params["title"] = request.form.get("title")
        params["author"] = request.form.get("author")
        params["publisher"] = request.form.get("publisher")
        params["owner"] = request.form.get("book_owner")
        params["isbn"] = request.form.get("isbn")
        params["pages"] = request.form.get("pages")
        params["category"] = request.form.get("category")
        params["description"] = request.form.get("description")
        params["state"] = request.form.get("state")

        b.update_book(request.form.get("bookid"), params)

        return render_template("update.html", text=b.show_books())
    return render_template("update.html", text=b.show_books())


@app.route("/delete", methods=["POST", "GET"])
def delete():
    """
    """

    if request.method == "POST":
        b = baza.Baza()
        b.delete_book(request.form.get("bookid"))

        return render_template("delete.html")
    return render_template("delete.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    """
    """
    b = baza.Baza()
    if request.method == "POST":
        params = {}
        params['name'] = request.form.get('name')
        params['surname'] = request.form.get('surname')
        params['mail'] = request.form.get('mail')
        params['phone'] = request.form.get('phone')

        b.add_reader(params)

        return render_template("user.html", text=b.show_users())
    return render_template("user.html", text=b.show_users())


@app.route("/books")
def books():
    """
    """

    b = baza.Baza()

    return render_template("books.html", text=b.show_books())


@app.route("/orders", methods=["POST", "GET"])
def orders():
    """
    """

    b = baza.Baza()
    if request.method == "POST":
        b.return_book(request.form.get('rentid'))

        return render_template("orders.html", text=b.show_orders())

    return render_template("orders.html", text=b.show_orders())


@app.route("/wishlist", methods=["POST", "GET"])
def wishlist():
    """
    """

    b = baza.Baza()
    if request.method == "POST":
        params = {}
        params["title"] = request.form.get("title")
        params["author"] = request.form.get("author")
        params["publisher"] = request.form.get("publisher")
        
        b.add_to_wishlist(params)

        return render_template("wishlist.html", text=b.show_wishlist())
    return render_template("wishlist.html", text=b.show_wishlist())


if __name__ == "__main__":
    from os import path, walk
    import os

    extra_dirs = [os.getcwd()]
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    app.run(extra_files=extra_files, host='0.0.0.0', debug=True)
