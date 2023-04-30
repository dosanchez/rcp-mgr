from datetime import datetime
from decimal import Decimal
import mysql.connector
from nav import navigate_to, nav_pos
from data import select as sel, update as upd, DataHandler as dth

#conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
#                               host='sql5.freesqldatabase.com',
#                               database='sql5514428')
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                               host='10.0.2.5',
                               database='rct')
db = conn.cursor(dictionary= True, buffered=True)


balance = sel.all_choices(db, 'wrh4returns', 'alm_name', blank = True, log_enca = 3, 
                          log_sku = 36) 
print('balance', balance or 'vacio')



conn.close()