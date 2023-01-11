import datetime
from decimal import Decimal
import mysql.connector
from nav import navigate_to, nav_pos
from forms import Almacen
from data import select as sel

#conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
#                               host='sql5.freesqldatabase.com',
#                               database='sql5514428')
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                               host='192.168.100.254',
                               database='rct')
db = conn.cursor(dictionary= True, buffered=True)
conn.close()

# a = {"g/unit": Decimal(1.02), "unit/g": Decimal(0.9803921568627451), 
#     "ml/unit": Decimal(1.09), "unit/ml": Decimal(0.9174311926605505), 
#     "g/ml": Decimal(0.9357798165137615), "ml/g": Decimal(1.0686274509803921)}
ingr= 5
sql = """('{0}gg',{0},'g','g',1), ('{0}mlml',{0},'ml','ml',1),
                        ('{0}unitunit',{0},'unit','unit',1)
                        ON DUPLICATE KEY UPDATE mtx_conv = values(mtx_conv)""".format(ingr)
print(sql)