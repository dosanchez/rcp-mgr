import datetime
from decimal import Decimal
import mysql.connector
from nav import navigate_to, nav_pos
from forms import Almacen
from data import select as sel, update as upd

#conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
#                               host='sql5.freesqldatabase.com',
#                               database='sql5514428')
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                               host='10.0.2.5',
                               database='rct')
db = conn.cursor(dictionary= True, buffered=True)

sql = """SELECT b.* FROM retur_en AS h INNER JOIN logix_de AS b
                ON h.id = b.log_rtrn
                WHERE h.id = '' """
db.execute(sql)
a = db.fetchall()
b = "\'\'"
print (b, type(b))
conn.close()
