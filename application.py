import os

from flask import Flask, session, render_template, request, jsonify, flash
import psycopg2 ##Connect to Heroku with ssl
from flask_session import Session
import json
import datetime
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#what is hard: psycopg (ssl required) Mysql in python, especially with % for 'like' they mean something else in python, I hate exception e.g. search need to be capitals
#What is easy => At the end of the assignment I could actually write multiple lines of code in python and HTML and it worked on first try
#Make nice: User login


#Params API
KEY = "MKXQATZ9XR0Mc2dJDyw01Q"
isbns = 9781632168146

app = Flask(__name__)
app.debug = True
DATABASE_URL="postgres://anxgkrduzonffo:870af2c45e8670df00a278345b73b5a2a915bc3a3a69aa067f130ddb0fb749@ec2-54-75-232-114.eu-west-1.compute.amazonaws.com:5432/d75mvmma11fn7f"

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
  # raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
#Sessions explained in movie lecture two last part 'notes'

# Set up database

#DATABASE_URL=os.environ['DATABASE_URL']
#conn=psycopg2.connect(DATABASE_URL, sslmode='require')

conn=psycopg2.connect(host="ec2-54-75-230-253.eu-west-1.compute.amazonaws.com", database="ddhqmc7s71fdfd", user="jshhhhyjozsciy", password="4cd98e27c32c3929124ca31c8947708756556b5582b0ff1fe66895990667c562",sslmode='require')
cur=conn.cursor()
#engine = create_engine(conn)
#db = scoped_session(sessionmaker(bind=engine))



@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user_id") is None:
        return render_template("/login.html")

    cur.execute("SELECT author, average_score, isbn, review_count, title,year FROM book b LIMIT 24;")
    searchResult = cur.fetchall()
    username = session["user_id"]
    return render_template("index.html", searchResult=searchResult, username=username)
    #  If is post
    """
        def getreview(KEY, isbns):
           resReview = requests.get("https://www.goodreads.com/book/review_counts.json",
                                    params={"key": KEY, "isbns": isbns})
           return resReview.text
"""

    def logout():
        # Forget any user_id
        session.clear()
        return render_template("login.html")

@app.route("/search", methods=["POST"])
def search():
    if session.get("user_id") is None:
        return render_template("/login.html")
    username = session["user_id"]
    search=request.form.get("search")
    cur.execute("SELECT author, average_score, isbn, review_count, title,year FROM book b where isbn like ('%%%s%%') or author like ('%%%s%%') or title like ('%%%s%%') LIMIT 48;"%(search,search,search))
    searchResult = cur.fetchall()
    return render_template("search.html", searchResult=searchResult, username=username)

    return render_template("error.html", message="Search result invalid")

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    if session.get("user_id") is None:
        return render_template("/login.html")

    if request.method == "GET":
        cur.execute("SELECT author, average_score, isbn, review_count, title,year, id FROM book b where isbn = '%s' ;"%isbn)
        #  Implement if query returns error
        bookDetail = cur.fetchone()
        GRReview = requests.get("https://www.goodreads.com/book/review_counts.json",
                                     params={"key": KEY, "isbns": isbn}).json()["books"][0]
        ##Implement errors
        ratingCount=GRReview["ratings_count"]
        avgRating=GRReview["average_rating"]

        ##reviews from website
        book_id=bookDetail[6]
        cur.execute("SELECT review_score, comment FROM review where book_id = '%s' LIMIT 24;"%book_id)
        reviewResult = cur.fetchall()
        return render_template("book.html", bookDetail = bookDetail, ratingCount=ratingCount, avgRating=avgRating , reviewResult=reviewResult)

    if request.method == "POST":
        visitorRating = request.form.get("rate")
        visitorComment = request.form.get("comment")
        if visitorRating is None or visitorComment is None:
            return render_template("error.html", message="Please provide rating and review")
        else:
            username = session["user_id"]
            cur.execute(
                "SELECT id FROM book b where isbn = '%s' ;" % isbn)
            #  Implement if query returns error
            bookId = cur.fetchone()
            bookId = bookId[0]
            #  Only allow a review if that user didn't review that same book before
            cur.execute(
                "SELECT * FROM review where book_id = %s AND visitor_id = %s;", (bookId, username))
                #"SELECT * FROM review where book_id = 3665 and visitor_id = 9;")
            testvar = cur.fetchone()
            if testvar is None:
                cur.execute("INSERT INTO review (book_id, review_score, visitor_id, comment) VALUES(%s, %s, %s, %s)", (bookId, visitorRating,username,visitorComment))
                conn.commit()
                return render_template("error.html", message="Thanks for leaving a review!")
            else:
                return render_template("error.html", message="You already reviewed this book")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Please provide username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="Please provide password")

        # Query database for username
        username=request.form.get("username")
        cur.execute("SELECT * FROM visitor WHERE username = '%s';"%username)
        rows=cur.fetchall()
        # Ensure username exists and password is correct or not request.form.get("password")
        if len(rows) != 1 or rows[0][1] != request.form.get("password"):
            return render_template("error.html", message="Invalid username or password")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return index()

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Please provide username")
        # Query database for username in order to check for existance
        username=request.form.get("username")
        cur.execute("SELECT * FROM visitor WHERE username = '%s';"%username)
        rows = cur.fetchall()

        # Check if username already exists
        if rows is not None and len(rows) != 0:
            return render_template("error.html", message="Username already exists")

        # ensure password was submitted
        elif not request.form.get("password") and request.form.get("password_conf"):
            return render_template("error.html", message="Please provide password")

        # make sure confirmation is password
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", message="Password not the same as confirmation")
        else:
            password = request.form.get("password")
            cur.execute("INSERT INTO visitor (username, password) VALUES(%s, %s)", (username, password))
            conn.commit()
            return render_template("index.html")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/api/<string:isbn>")
def api(isbn):
    cur.execute(
        "SELECT author, average_score, isbn, review_count, title,year, id FROM book b where isbn = '%s' ;" % isbn)
    bookDetail = cur.fetchone()
    cur.execute(
        "SELECT count(review_score) as count_score_review , sum(review_score) as sum_score_review FROM review where book_id = '%s' ;" % bookDetail[6])
    bookReview = cur.fetchone()
    AvgReview = bookReview[1] / bookReview[0]
    bookDetail = {
        "Title": bookDetail[4],
        "Author": bookDetail[0],
        "Year": bookDetail[5],
        "isbn": bookDetail[2],
        "review_count": bookReview[0],
        "Average_score": AvgReview
    }
    
    bookDetail = json.dumps(bookDetail, indent=4, separators=(',', ': '))

    #bookDetail = jsonify(Title=bookDetail[4], Author=bookDetail[0], Year=bookDetail[5], isbn=bookDetail[2])
    print(bookDetail)
    return render_template("api.html", bookDetail=bookDetail)

@app.route("/error")
def error():
    """Define error message"""
    return render_template("error.html")