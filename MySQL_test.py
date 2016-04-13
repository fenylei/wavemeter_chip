import MySQLdb as mdb
import sys
import random
import time, datetime
import math

con = mdb.connect('127.0.0.1', 'python','mtQg116sc','wavemeter')

cur = con.cursor()

insert_stmt = (
  "INSERT INTO error (emp_no, first_name, last_name, hire_date) "
  "VALUES (%s, %s, %s, %s)"
)
data = (2, 'Jane', 'Doe', datetime.date(2012, 3, 23))
cur.execute(insert_stmt, data)
