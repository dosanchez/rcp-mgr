from datetime import datetime
from decimal import Decimal
import mysql.connector
from nav import navigate_to, nav_pos
from forms import Almacen, Return_en
from data import select as sel, update as upd

#conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
#                               host='sql5.freesqldatabase.com',
#                               database='sql5514428')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                                host='10.0.2.5',
#                                database='rct')
# db = conn.cursor(dictionary= True, buffered=True)


 
b = "Tue, 03 Jan 2023 00:00:00 GMT"

a = datetime.strptime(b, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
print (a, type(a))
# conn.close()
