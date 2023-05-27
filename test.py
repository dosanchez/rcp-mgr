from datetime import datetime
from decimal import Decimal
import mysql.connector
from nav import navigate_to, nav_pos
from data import select as sel, update as upd, DataHandler as dth

# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                                host='129.213.87.97',
#                                database='rct')
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                              host='192.168.100.254',
                              database='rct')
db = conn.cursor(dictionary= True, buffered=True)


a = None
if not a == None:  
    print('true')
else:
    print('false')

conn.close()