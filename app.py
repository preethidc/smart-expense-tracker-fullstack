from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def index():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            note TEXT
        )
    """)

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        note = request.form["note"]

        cursor.execute("INSERT INTO expenses (amount, category, note) VALUES (?, ?, ?)",
                       (amount, category, note))
        db.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    total = sum([x[1] for x in expenses])

    return render_template("index.html", expenses=expenses, total=total)

@app.route("/delete/<int:id>")
def delete(id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,
host="0.0.0.0")