import os

from flask import Flask, session, render_template
import psycopg2 ##Connect to Heroku with ssl
from flask_session import Session
import datetime
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#Params API
KEY = "MKXQATZ9XR0Mc2dJDyw01Q"
isbns = 9781632168146
#searchword = "Harry"

app = Flask(__name__)
app.debug = True
#DATABASE_URL="postgres://anxgkrduzonffo:870af2c45e8670df00a278345b73b5a2a915bc3a3a69aa067f130ddb0fb749@ec2-54-75-232-114.eu-west-1.compute.amazonaws.com:5432/d75mvmma11fn7f"
# Check for environment variable
#if not os.getenv("DATABASE_URL"):
  # raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"

#Session(app)
#Sessions explained in movie lecture two last part 'notes'

# Set up database

DATABASE_URL=os.environ['DATABASE_URL']
#conn=psycopg2.connect(DATABASE_URL, sslmode='require')
conn=psycopg2.connect(host="ec2-54-75-232-114.eu-west-1.compute.amazonaws.com", database="d75mvmma11fn7f", user="anxgkrduzonffo", password="870af2c45e8670df00a278345b73b5a2a915bc3a3a69aa067f130d9ddb0fb749",sslmode='require')
cur=conn.cursor()
#engine = create_engine(conn)
#db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    #searchResult=conn.execute("SELECT * FROM book").fetchall()
    cur.execute("SELECT author, average_score, isbn, review_count, title,year FROM book b;")
    searchResult = cur.fetchall()
    print(searchResult)

    def getreview(KEY, isbns):
       resReview = requests.get("https://www.goodreads.com/book/review_counts.json",
                                params={"key": KEY, "isbns": isbns})
       return resReview.text
       print(resReview.text)

    resReview=getreview(KEY, isbns)
    return render_template("index.html", searchResult=searchResult, resReview=resReview)

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
