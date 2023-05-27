from flask import session
from flask import redirect  
from data import select as sel
import decimal

def nav_pos(rcds, id, nav_button):
#resolve list index value of navigation target record (if any rcd)

    regd_id =[row.get('id') for row in rcds] #making a list of registered ids
    last_index = len(regd_id) -1 #calc id list length

    if not len(regd_id) or regd_id == [None]:
        return 0, []
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
        return 0, regd_id
    else:
        return -1, regd_id    

def navigate_to(nav_button, conn, form, table_list, **kwargs):
    """visualize registered U.M and moves form to nav target"""
    rcds =[]
    relation=[]
    counter = 0
    db = conn.cursor(dictionary=True, buffered=True)
    while counter < len(table_list):
        if counter == 0:

            if not kwargs:
                rcds.append(sel.all(db, table_list[counter]))
                res = sel.max_id(db, table_list[counter])
            #the kwargs part is used for considering only a subset of records
            #in the header.  Ingredient and recipe forms share the same 
            #SQL Table == recet_en, hence need to discriminate for returns only
            # returns related to a certain reception are displayed
            else: 
                rcds.append(sel.all(db, table_list[counter], **kwargs))
                res = sel.max_id(db, table_list[counter], **kwargs)

            session['parent_last_row_id'] = res[0].get('parent_last_row_id')
            id = form.id.data
            
            pos, regd_id = nav_pos(rcds[counter], id, nav_button)
            counter += 1

        #visualize the target record on main form (if any rcd)
        if not len(regd_id):
            counter += 1

        else:

            tgt_record = rcds[0][pos]
            session['curr_rcd_' + type(form).__name__] = tgt_record.get('id')
            
            #exception for return form
            if table_list[0] == 'return_header':
                ref_tbl = 'retur_en'
            else:
                ref_tbl = table_list[0]

            for i in form:
                if not i.id == 'csrf_token':
                    if i.id == "qty_um" and table_list[0] == 'unitmeas':#exception for unitmeas form
                        i.data = 1
                    elif i.id == "qty_base" and table_list[0] == 'unitmeas':#exception for unitmeas form
                        i.data = session['uni_conv'] = tgt_record.get('uni_conv')
                    elif type(i).__name__ == 'FormField':

                        relation.append(sel.foreign_tbl(conn, ref_tbl,
                                                        table_list[counter]))
                        
                        #turns inexistent first record id into '' for sql
                        if not tgt_record.get('id'):
                            tgt_record['id'] = "\'\'"

                        subform_rcds = sel.chld_vals(db, ref_tbl, table_list[counter],
                                relation[counter-1][0].get('child_tbl_fld'),
                                tgt_record.get('id'))
                        #print('subform_rcds', subform_rcds)
                        #first time subform entry
                        if subform_rcds:
                            rcds.append(subform_rcds)
                        else:
                            rcds.append([{}])

                        pos, regd_id = nav_pos(rcds[counter],
                            i.idx.data, session['sub_nav_button'])

                        for ii in i:
                            if ii.short_name == 'idx':
                                fld_tbl = 'id'
                            else:
                                fld_tbl = ii.short_name
                            
                            #makes None values null string for html form field value
                            session[ii.short_name] = rcds[counter][pos].get(fld_tbl)
                            
                            if not session[ii.short_name]:
                                ii.data = ii.default or ''
                            else:
                                #print(ii.short_name +' ----->',type(session[ii.short_name]) == (int or float) or (type(session[ii.short_name]) is decimal.Decimal))
                                if type(session[ii.short_name]) == (int or float) or (type(session[ii.short_name]) is decimal.Decimal):
                                    ii.data = abs(session[ii.short_name])
                                else:
                                    ii.data = session[ii.short_name]
                        counter += 1

                    else:
                        #makes None values null string for html form field value
                        session[i.id] = tgt_record.get(i.id)
                        

                        if not session[i.id]:
                            i.data = i.default or ''
                        else:
                            i.data = session[i.id]
                            if type(session[i.id]) == int or type(session[i.id]) == float:
                                i.data = abs(session[i.id])
                            else:
                                i.data = session[i.id]                     
    return rcds, relation