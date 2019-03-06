import os

from flask import Flask, session, render_template
from flask_session import Session
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.debug = True

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
 #  raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"

#Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book/<string:name>")
def book(name):
    now=datetime.datetime.now()
    return render_template("book.html",name=name, now=now)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")