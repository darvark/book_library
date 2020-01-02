from flask import Flask
from flask import render_template
from flask import request, json

import baza
import test_data

app = Flask(__name__)

# test_data.add_test_data()

@app.route("/")
def home():
    """
    """

    return render_template("home.html")
    

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


@app.route("/books")
def books():
    """
    """
    return render_template("books.html")


@app.route("/api/books", methods=["POST", "GET"])
def get_books():
    b = baza.Baza()
    return json.jsonify({"books": b.get_all_books()})


@app.route("/book/add", methods=["POST"])
def add_book():
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
    book = b.add_book(params)

    return json.jsonify(book)


@app.route("/book/edit", methods=["POST"])
def edit_book():
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
    book = b.update_book(request.form.get("book_id"), params)
    return json.jsonify(book)


@app.route("/book/delete", methods=["DELETE"])
def delete():
    """
    """

    if request.method == "DELETE":
        b = baza.Baza()
        book = b.delete_book(request.form.get("book_id"))
        return json.jsonify(book)


@app.route("/users", methods=["POST", "GET"])
def users():
    """
    """
    return render_template("users.html")


@app.route("/api/users", methods=["POST", "GET"])
def get_users():
    b = baza.Baza()
    return json.jsonify({"users": b.get_all_readers()})


@app.route("/user/add", methods=["POST"])
def add_user():
    if request.method == "POST":
        params = {}
        params['name'] = request.form.get('name')
        params['surname'] = request.form.get('surname')
        params['mail'] = request.form.get('mail')
        params['phone'] = request.form.get('phone')

        b = baza.Baza()
        user = b.add_reader(params)

        return json.jsonify(user)


@app.route("/user/edit", methods=["POST"])
def edit_user():
    if request.method == "POST":
        params = {}
        params['name'] = request.form.get('name')
        params['surname'] = request.form.get('surname')
        params['mail'] = request.form.get('mail')
        params['phone'] = request.form.get('phone')

        b = baza.Baza()
        user = b.update_reader(request.form.get("user_id"), params)
        
        return json.jsonify(user)


@app.route("/user/delete", methods=["DELETE"])
def delete_user():
    """
    """

    if request.method == "DELETE":
        b = baza.Baza()
        user = b.delete_reader(request.form.get("user_id"))
        
        return json.jsonify(user)


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
    app.run(extra_files=extra_files, debug=True)