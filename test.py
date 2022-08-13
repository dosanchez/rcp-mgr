import mysql.connector
from nav import navigate_to

# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                        #       host='192.168.100.254',
                        #       database='std')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='200.125.169.75',
#                               database='std')
# db = conn.cursor(dictionary=True, buffered=True)

# sql ="""SELECT TABLE_NAME AS child_tbl, 
#                             COLUMN_NAME AS child_tbl_fld, 
#                             REFERENCED_TABLE_NAME AS parent_tbl, 
#                             REFERENCED_COLUMN_NAME AS parent_tbl_fld 
#                             FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
#                             WHERE TABLE_SCHEMA = 'std'
#                             AND REFERENCED_TABLE_NAME IS NOT NULL """
# db.execute(sql)
# relation = db.fetchall()
relation = [[{}]]

print (relation[0][0].get('a'))

# conn.close()