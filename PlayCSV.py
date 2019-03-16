import os
import pandas as pd
import psycopg2

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#def bulkUploadBooks():len(newbooks.index)
DATABASE_URL = "postgres://anxgkrduzonffo:870af2c45e8670df00a278345b73b5a2a915bc3a3a69aa067f130ddb0fb749@ec2-54-75-232-114.eu-west-1.compute.amazonaws.com:5432/d75mvmma11fn7f"

conn=psycopg2.connect(host="ec2-54-75-232-114.eu-west-1.compute.amazonaws.com", database="d75mvmma11fn7f", user="anxgkrduzonffo", password="870af2c45e8670df00a278345b73b5a2a915bc3a3a69aa067f130d9ddb0fb749",sslmode='require')
cur=conn.cursor()

#len(newbooks.index)-1
newbooks = pd.read_csv('books.csv', index_col=0)
for book in range (0,50):
    #id=4
    author=newbooks.ix[book, "author"]
    title=newbooks.ix[book, "title"]
    year=newbooks.ix[book, "year"].astype(str)
    isbn=newbooks.index[book]
    print(isbn)
    cur.execute("INSERT INTO book (isbn, title, author, year) VALUES (%s, %s, %s, %s)",(isbn, title, author, year))
conn.commit()
    #print(newbooks.ix[book, "isbn"])





