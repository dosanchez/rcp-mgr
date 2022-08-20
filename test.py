import mysql.connector
from nav import navigate_to

# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                        #       host='192.168.100.254',
                        #       database='std')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='200.125.169.75',
#                               database='std')
# db = conn.cursor(dictionary=True, buffered=True)


# sql = """SELECT MAX(id) AS parent_last_row_id
#         FROM unitmeas"""

def nav_pos():
        regd_id =[row for row in range(10)]
        return regd_id

print(nav_pos())



# conn.close()