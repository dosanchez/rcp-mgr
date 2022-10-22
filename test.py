import json
from decimal import Decimal
import mysql.connector
from nav import navigate_to, nav_pos
from forms import Almacen
from data import select as sel

# conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
#                               host='sql5.freesqldatabase.com',
#                               database='sql5514428')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='192.168.100.254',
#                               database='std')
# db = conn.cursor(dictionary=True, buffered=True)


c = Decimal(15)
print(type(c).__name__)
c = float(c)
a = 'hola'
b = json.dumps(a)
d = json.dumps(c)
print(b, d)

a = [{'ana':15.6, 'jose':None }]
a = dumps(a)
print(type(a))


#print([('','')].append((2,2)))
# print ('blank', blank)
# print('a', a)
# conn.close