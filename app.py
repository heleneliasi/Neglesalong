from flask import Flask, render_template, request, redirect, session, flash
from db import get_connection
import os
import mariadb
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dette-er-en-temp-secret")


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)  #last .env fila
env_User = os.getenv("DB_USER")
env_Host = os.getenv("DB_HOST")
env_Password = os.getenv("DB_PASSWORD")
env_Database = os.getenv("DB_NAME")

def get_connection():
    return mariadb.connect(
        host = env_Host,
        user = env_User,
        password = env_Password,
        database = env_Database
    )

@app.route("/")
def index():
    return render_template("index.html")


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
        passord = request.form["password"]
        service_id = request.form["service"]
        date = request.form["dato"]
        time = request.form["tid"]

        #legger til en bruker
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (navn, email, passord)
        )
        mydb.commit()
        user_id = cursor.lastrowid


        session["user_id"] = user_id
        session["username"] = navn

        #legg til time bestilt
        cursor.execute(
            "INSERT INTO appointment (user_id, service_id, date, time) VALUES (%s, %s, %s, %s)",
            (user_id, service_id, date, time)
        )
        mydb.commit()
        


        flash("Tusen takk for bestillingen! Vi gleder oss til å se deg <3")

        return redirect("/book")
    

    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    mydb.close()

    return render_template("book.html", services=services)


if __name__ == "__main__":
    app.run(debug=True)
