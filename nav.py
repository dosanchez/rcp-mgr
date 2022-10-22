from decimal import Decimal
import json
from flask import session
from flask import render_template
from data import select as sel

def nav_pos(rcds, id, nav_button):
#resolve list index value of navigation target record (if any rcd)

    regd_id =[row.get('id') for row in rcds] #making a list of registered ids
    last_index = len(regd_id) -1 #calc id list length
    if not len(regd_id):
        return None, []
    elif isinstance(nav_button,(int)):
        return regd_id.index(nav_button), regd_id
    elif id == None:
        return -1, regd_id    
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

def navigate_to(nav_button, conn, form, table_list):
    """visualize registered U.M and moves form to nav target"""
    rcds =[]
    relation=[]
    counter = 0
    db = conn.cursor(dictionary=True, buffered=True)
    while counter < len(table_list):
        if counter == 0:

            #Ingredient and recipe forms share the same SQL Table == recet_en, hence need to discriminate
            if type(form).__name__ == 'Ingredient':
                rcds.append(sel.all(db, table_list[counter], rct_rece = 0))
                res = sel.max_id(db, table_list[counter], rct_rece = 0)
            elif type(form).__name__ == 'Recet_en':
                rcds.append(sel.all(db, table_list[counter], rct_rece = 1))
                res = sel.max_id(db, table_list[counter], rct_rece = 1) 
            else:
                rcds.append(sel.all(db, table_list[counter]))
                res = sel.max_id(db, table_list[counter])

            session['parent_last_row_id'] = res[0].get('parent_last_row_id')
            id = form.id.data
            print('counter', counter)
            print('type rcds', type(rcds))
            print(rcds)

            pos, regd_id = nav_pos(rcds[counter], id, nav_button)
            counter += 1
        #visualize the target record on main form (if any rcd)
        if not len(regd_id):
            counter += 1
            pass
        else:

            tgt_record = rcds[0][pos]
            session['curr_rcd_' + type(form).__name__] = tgt_record.get('id')
            for i in form:
                if not i.id == 'csrf_token':
                    if i.id == "qty_um" and table_list[0] == 'unitmeas':#exception for unitmeas form
                        i.data = 1
                    elif i.id == "qty_base" and table_list[0] == 'unitmeas':#exception for unitmeas form
                        i.data = session['uni_conv'] = json.dumps(float(tgt_record.get('uni_conv')))
                    elif type(i).__name__ == 'FormField':

                        relation.append(sel.foreign_tbl(conn, table_list[0], table_list[counter]))

                        subform_rcds = sel.chld_vals(db, table_list[0], table_list[counter],
                                relation[counter-1][0].get('child_tbl_fld'), tgt_record.get('id'))

                        #first time subform entry
                        if subform_rcds:
                            rcds.append(subform_rcds)
                        else:
                            rcds.append([{}])

                        pos, regd_id = nav_pos(rcds[counter], i.idx.data, session['sub_nav_button'])

                        for ii in i:
                            if ii.short_name == 'idx':
                                fld_tbl = 'id'
                            else:
                                fld_tbl = ii.short_name
                            
                            #makes None values null string for html form field value
                            ii.data = rcds[counter][pos].get(fld_tbl)
                            session[ii.short_name] = ii.data
                            if rcds[counter][pos].get(fld_tbl) == None:
                                ii.data = ''
                            else:
                                ii.data = session[ii.short_name]

                        counter += 1
                    else:
                        #makes None values null string for html form field value
                        session[i.id] = tgt_record.get(i.id)
                        if tgt_record.get(i.id) == None:
                            i.data = ''
                        else:
                            i.data = session[i.id]
    return rcds, relation