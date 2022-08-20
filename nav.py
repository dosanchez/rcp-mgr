import mysql.connector
from flask import session
from flask import render_template
from data import select as sel

def nav_pos(rcds, id, nav_button):
#resolve list index value of navigation target record (if any rcd)

    regd_id =[row.get('id') for row in rcds] #making a list of registered ids
    last_index = len(regd_id) -1 #calc id list length

    if not len(regd_id):
        pass
    elif id == None:
        return -1, regd_id
    elif isinstance(nav_button,(int)):
        return regd_id.index(nav_button), regd_id
    elif nav_button == "first":
        return 0, regd_id
    elif nav_button == "last":
        return -1, regd_id
    elif nav_button == "back" and regd_id.index(int(id)) > 0:
        return regd_id.index(int(id)) - 1, regd_id
    elif nav_button == "back" and regd_id.index(int(id)) == 0:
        return 0, regd_id
    elif nav_button == "next" and regd_id.index(int(id)) < last_index:
        return regd_id.index(int(id)) + 1, regd_id
    elif nav_button == "next" and regd_id.index(int(id)) == last_index:
        return -1, regd_id
    elif nav_button == "out":
        return render_template ('index.html')
    else:
        return -1, regd_id    

def navigate_to(nav_button, db, form, table_list):
    """visualize registered U.M and moves form to nav target"""
    rcds =[]
    relation=[]
    counter = 0
    while counter < len(table_list):
        if counter == 0:   
            rcds.append(sel.all(db, table_list[counter]))

            res = sel.max_id(db, table_list[counter])
            session['parent_last_row_id'] = res[0].get('parent_last_row_id')
            id = form.id.data

            pos, regd_id = nav_pos(rcds[counter], id, nav_button)
            counter += 1
        

        #visualize the target record on main form (if any rcd)
        if not len(regd_id):
            counter += 1
            pass
        else:

            tgt_record = rcds[0][pos]

            for i in form:
                if not i.id == 'csrf_token':
                    if i.id == "qty_um" and table_list[0] == 'unitmeas':#exception for unitmeas form
                        i.data = 1
                    elif i.id == "qty_base" and table_list[0] == 'unitmeas':#exception for unitmeas form
                        i.data = session['uni_conv'] = tgt_record.get('uni_conv')
                    elif type(i).__name__ == 'FormField':
                        sql ="""SELECT TABLE_NAME AS child_tbl, 
                            COLUMN_NAME AS child_tbl_fld, 
                            REFERENCED_TABLE_NAME AS parent_tbl, 
                            REFERENCED_COLUMN_NAME AS parent_tbl_fld 
                            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = 'std'
                            AND REFERENCED_TABLE_NAME = '{}'
                            AND TABLE_NAME = '{}'
                            AND REFERENCED_COLUMN_NAME = 'id'""".format(table_list[0]
                            , table_list[counter])
                        db.execute(sql)
                        relation.append(db.fetchall())


                        sql = """SELECT b.* FROM {} AS h INNER JOIN {} AS b
                                ON h.id = b.{}
                                WHERE h.id = {}""".format(table_list[0],
                                table_list[counter],
                                relation[counter-1][0].get('child_tbl_fld'),
                                tgt_record.get('id'))
                        db.execute(sql)
                        a = db.fetchall()

                        #first time subform entry
                        if a:
                            rcds.append(a)
                        else:
                            rcds.append([{}])

                        pos, regd_id = nav_pos(rcds[counter], i.idx.data, session['sub_nav_button'])

                        for ii in i:
                            if ii.short_name == 'idx':
                                fld_tbl = 'id'
                            else:
                                fld_tbl = ii.short_name

                            ii.data = session[ii.short_name] = rcds[counter][pos].get(fld_tbl)

                        counter += 1
                    else:
                        i.data = session[i.id] = tgt_record.get(i.id)
    return rcds, relation