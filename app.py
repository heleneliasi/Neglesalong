<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, session
import mariadb
=======
from flask import Flask,
render_template, request, redirect, session
>>>>>>> d925abce4951de774f24f4b68c2491526555cb34
from datetime import datetime

app = Flask(__name__)
app.secret_key = "spaghetti"
