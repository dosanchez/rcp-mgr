import mysql.connector

conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                              host='192.168.100.254',
                              database='std')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='200.125.169.75',
#                               database='std')
db = conn.cursor(dictionary=True, buffered=True)

sql = "Select * from ingredient"
db.execute(sql)
records = db.fetchall()
conn.close()


print (type(records))
print (records)
print(records[0]['ing_dens'])