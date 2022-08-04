import mysql.connector
from flask import session
from flask_wtf import FlaskForm
from flask import render_template
from forms import Unitmeas


def navigate_to(nav_button, db, form, sqltable):

    #visualize registered U.M and moves form to nav target

    sql = "Select * from {}".format(sqltable) 
    db.execute(sql)
    records = db.fetchall()
    # column_names = db.column_names

    regd_id =[row.get('id') for row in records] #making a list of registered ids
    last_index = len(regd_id) -1 #calc id list length
    
    #checks for first time form entry (parent form)
    if form.id.data:
        id = form.id.data
    else:
        id = form.id.data = 0

    #checks for first time form entry (child form)
    if form.subform.idx.data:
        subid = form.subform.idx.data
    else:
        try:
            subid = form.subform.idx.data = 0
        except:
            pass

    #resolve id value of navigation target record (if any rcd)
    if not len(regd_id):
        pass
    elif id == None:
        id = regd_id[-1]
    elif isinstance(nav_button,(int)):
        id = nav_button
    elif nav_button == "first":
        id = regd_id[0] 
    elif nav_button == "last":
        id = regd_id[-1]
    elif nav_button == "back" and regd_id.index(int(id)) > 0:
        id = regd_id[regd_id.index(int(id)) - 1]
    elif nav_button == "back" and regd_id.index(int(id)) == 0:
        id = regd_id[0]
    elif nav_button == "next" and regd_id.index(int(id)) < last_index:
        id = regd_id[regd_id.index(int(id)) + 1]
    elif nav_button == "next" and regd_id.index(int(id)) == last_index:
        id = regd_id[-1]
    elif nav_button == "out":
        return render_template ('index.html')
    else:
        id = regd_id[-1]
    

    #visualize the target record on main form (if any rcd)
    if not len(regd_id):
        pass
    else:
        sql = "SELECT * FROM %s WHERE id = %s"%(sqltable, id)
        db.execute(sql)
        tgt_record = db.fetchone()

        for i in form:
            if not i.id == 'csrf_token':
                    if i.id == "qty_um" and sqltable == 'unitmeas':#exception for unitmeas form
                        i.data = 1
                    elif i.id == "qty_base" and sqltable == 'unitmeas':#exception for unitmeas form
                        i.data = session['uni_conv'] = tgt_record.get('uni_conv')
                    else:
                        print(i)
                        i.data = session[i.id] = tgt_record.get(i.id)

        tgt_record = db.fetchall()

    return records