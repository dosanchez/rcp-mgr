from traceback import format_exc
import mysql.connector
from nav import navigate_to, nav_pos
from forms import Almacen

conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
                              host='sql5.freesqldatabase.com',
                              database='sql5514428')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='200.125.169.75',
#                               database='std')
# db = conn.cursor(dictionary=True, buffered=True)


# sql = """SELECT MAX(id) AS parent_last_row_id
#         FROM unitmeas"""

form = Almacen()

def all(tbl, **filter):
        """returns all records from a given table"""
        if not filter:
            sql = "Select * from {}".format(tbl)
            return(sql)
        else:
            sql = "SELECT * FROM {} WHERE ".format(tbl)
            for field, value in filter.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(field, value)
                else:
                    sql += "{} ='{} ".format(field, value)
                sql += "AND "
            sql[:-4] # Slice string to remove last character from string
        return (sql[:-4])

print(all('tabla', resp ='bien', vecino = 'malapaga'))

match (100, 200):
    case (100, 300):  # Mismatch: 200 != 300
        print('Case 1')
    case (100, 200) if flag:  # Successful match, but guard fails
        print('Case 2')
    case (100, y):  # Matches and binds y to 200
        print(f'Case 3, y: {y}')
    case _:  # Pattern not attempted
        print('Case 4, I match anything!')
        
form_name = 'Ingredient'
match form_name:
    case 'Ingredient':
        print('Ingrediente')
    case 'recet_en':
        print('receten')
    case _:
        print('otro')



conn.close()