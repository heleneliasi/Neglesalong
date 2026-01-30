from flask import Flask, render_template, request, redirect, session
import mariadb
from datetime import datetime

app = Flask(__name__)
app.secret_key = "veldghemmelig123"
