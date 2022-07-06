
import mysql.connector

conn = mysql.connector.connect(
    host= "DiskStation" #"192.168.100.254"
    port = 3307
    user="rcp"
    password="yM9-F7bVUA"
    database:"std"
)

db = conn.cursor()

