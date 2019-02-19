import mysql.connector

cnx = mysql.connector.connect(
    user='root', 
    password='root1234', 
    host='127.0.0.1', 
    database='mydb')

class DBConnector:
    def __init__(self):
        print("hello from init")

    def getName(self):
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * FROM Patient")
        cursor.execute(query)

        cursor.close()
        cnx.close()

        print("name...")



