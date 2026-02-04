from flask import Flask, render_template, request, redirect
from db import get_connection

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ping")
def ping():
    conn = get_connection()

    if conn:
        return "200" 
    
    return "Conn funker ikke"

@app.route("/services")
def services_page():
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    mydb.close()
    return render_template("services.html", services=services)


@app.route("/book", methods=["GET", "POST"])
def book_page():
    mydb = get_connection()
    cursor = mydb.cursor()

    if request.method == "POST":
        navn = request.form["navn"]
        email = request.form["email"]
        service_id = request.form["service"]
        dato = request.form["dato"]

        # legg til bruker
        cursor.execute(
            "INSERT INTO user (name, email) VALUES (%s, %s)",
            (navn, email)
        )
        mydb.commit()
        user_id = cursor.lastrowid

        # legg til time
        cursor.execute(
            "INSERT INTO appointment (user_id, service_id, date) VALUES (%s, %s, %s)",
            (user_id, service_id, dato)
        )
        mydb.commit()

        mydb.close()
        return redirect("/")

    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    mydb.close()

    return render_template("book.html", services=services)


if __name__ == "__main__":
    app.run(debug=True)
