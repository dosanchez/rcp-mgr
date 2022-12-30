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

a = {"g/unit": Decimal(1.02), "unit/g": Decimal(0.9803921568627451), 
    "ml/unit": Decimal(1.09), "unit/ml": Decimal(0.9174311926605505), 
    "g/ml": Decimal(0.9357798165137615), "ml/g": Decimal(1.0686274509803921)}


b = sel.UMconv(db,1,'g','unit', matrix=a)
print(b)
# if 'd' in a.keys():
#     print('si')
# else:
#     print('no')

# sel.chkmissingdens(conn, ingr = 64)

# sql ="""WITH unit AS (

#                         SELECT sku_ingr, uni_un_t
#                         FROM sku
#                         LEFT JOIN unitmeas
#                         ON sku_unit = unitmeas.id)

#                     SELECT DISTINCT uni_un_t AS unit, rct_dens AS dens, rct_denu AS denu, 
#                                 rct_dens_1 AS dens1, rct_denu_1 AS denu1, rct_name, recet_en.id
#                     FROM recet_en
#                     LEFT JOIN unit
#                     ON recet_en.id = sku_ingr
#                     WHERE recet_en.id = 32"""
# db.execute(sql)
# a= db.fetchall()
# print(a)