import datetime
from decimal import Decimal
import mysql.connector
from nav import navigate_to, nav_pos
from forms import Almacen
from data import select as sel

conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
                               host='sql5.freesqldatabase.com',
                               database='sql5514428')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='192.168.100.254',
#                               database='std')
db = conn.cursor(dictionary=True, buffered=True)


#print(sel.sumfields(db, 'recet_de','rcd_qty','rcd_yiel',rcd_enca=28))
print(sel.all(db, 'logix_en'))







#print([('','')].append((2,2)))
# print ('blank', blank)
# print('a', a)
# conn.close