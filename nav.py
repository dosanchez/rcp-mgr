import mysql.connector
from flask import session
from flask_wtf import FlaskForm
from flask import render_template
from forms import Unitmeas


def navigate_to(nav_button, db, form, sqltable):
    """visualize registered U.M and moves form to nav target"""

    sql = "Select * from {}".format(sqltable) 
    db.execute(sql)
    records = db.fetchall()

    regd_id =[row.get('id') for row in records] #making a list of registered ids
    last_index = len(regd_id) -1 #calc id list length
 

    #resolve list index value of navigation target record (if any rcd)
    if not len(regd_id):
        pass
    elif id == None:
        pos = -1
    elif isinstance(nav_button,(int)):
        pos = regd_id.index(nav_button)
    elif nav_button == "first":
        pos = 0
    elif nav_button == "last":
        pos = -1
    elif nav_button == "back" and regd_id.index(int(id)) > 0:
        pos = regd_id.index(int(id)) - 1
    elif nav_button == "back" and regd_id.index(int(id)) == 0:
        pos = 0
    elif nav_button == "next" and regd_id.index(int(id)) < last_index:
        pos = regd_id.index(int(id)) + 1
    elif nav_button == "next" and regd_id.index(int(id)) == last_index:
        pos = -1
    elif nav_button == "out":
        return render_template ('index.html')
    else:
        pos = -1
        
    #id = regd_id[pos]
    

    #visualize the target record on main form (if any rcd)
    if not len(regd_id):
        pass
    else:
        tgt_record = records[pos]

        for i in form:
            if not i.id == 'csrf_token':
                    if i.id == "qty_um" and sqltable == 'unitmeas':#exception for unitmeas form
                        i.data = 1
                    elif i.id == "qty_base" and sqltable == 'unitmeas':#exception for unitmeas form
                        i.data = session['uni_conv'] = tgt_record.get('uni_conv')
                    elif type(i).__name__ == 'FormField':

                        print('Hola Formfield', i.id, type(i.id))
                    else:
                        print(type(i).__name__)
                        i.data = session[i.id] = tgt_record.get(i.id)

        

    return records