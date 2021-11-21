import streamlit as st
import MySQLdb

st.title("Hello again, to all my friends")


# Connect
db = MySQLdb.connect(host="db",
                     user="test",
                     passwd="test123",
                     db="test")
# config = {
#         'user': 'test',
#         'password': 'test123',
#         'host': 'db',
#         'port': '3306',
#         'database': 'test'
#     }
# connection = mysql.connector.connect(**config)

st.write("Here's our first attempt ")
cursor = db.cursor()
cursor.execute("USE test")
cursor.execute("SHOW TABLES;")

st.write(str(cursor.fetchall()))


# Close the connection
db.close()