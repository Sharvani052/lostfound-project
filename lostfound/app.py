from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def init_db():
    conn = sqlite3.connect("items.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        location TEXT,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    search = request.args.get("search")

    conn = sqlite3.connect("items.db")
    c = conn.cursor()

    if search:
        c.execute("SELECT * FROM items WHERE name LIKE ?", ('%'+search+'%',))
    else:
        c.execute("SELECT * FROM items")

    items = c.fetchall()
    conn.close()

    return render_template("index.html", items=items)


@app.route("/report", methods=["GET","POST"])
def report():
    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]
        location = request.form["location"]
        item_type = request.form["type"]

        conn = sqlite3.connect("items.db")
        c = conn.cursor()

        c.execute(
        "INSERT INTO items(name,description,location,type) VALUES(?,?,?,?)",
        (name,description,location,item_type)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("report.html")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USER and password == ADMIN_PASS:
            return redirect("/admin")

    return render_template("login.html")


@app.route("/admin")
def admin():

    conn = sqlite3.connect("items.db")
    c = conn.cursor()

    c.execute("SELECT * FROM items")
    items = c.fetchall()

    conn.close()

    return render_template("admin.html", items=items)


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("items.db")
    c = conn.cursor()

    c.execute("DELETE FROM items WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
