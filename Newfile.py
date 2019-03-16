import os
import pandas as pd
import psycopg2
import csv

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#def bulkUploadBooks():len(newbooks.index)
DATABASE_URL = "postgres://anxgkrduzonffo:870af2c45e8670df00a278345b73b5a2a915bc3a3a69aa067f130ddb0fb749@ec2-54-75-232-114.eu-west-1.compute.amazonaws.com:5432/d75mvmma11fn7f"

conn=psycopg2.connect(host="ec2-54-75-232-114.eu-west-1.compute.amazonaws.com", database="d75mvmma11fn7f", user="anxgkrduzonffo", password="870af2c45e8670df00a278345b73b5a2a915bc3a3a69aa067f130d9ddb0fb749",sslmode='require')
cur=conn.cursor()

openbooks = open("books.csv")
newbooks = csv.reader(openbooks)
print(newbooks)

for isbn, title, author, year in newbooks:
 #   cur.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})

#cur.commit()

#newbooks.to_sql(con=conn, name='book', if_exists='replace')





