from traceback import format_exc
import mysql.connector
from nav import navigate_to, nav_pos
from forms import Almacen

# conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
#                               host='sql5.freesqldatabase.com',
#                               database='sql5514428')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='200.125.169.75',
#                               database='std')
# db = conn.cursor(dictionary=True, buffered=True)


# sql = """SELECT MAX(id) AS parent_last_row_id
#         FROM unitmeas"""



choice = (1,1)
blank = [('','')]
a= blank.append(choice)

#print([('','')].append((2,2)))
print ('blank', blank)
print('a', a)
# conn.close