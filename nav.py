import mysql.connector


def tg_id(id, nav_button,regd_id):
    #resolve id value of navigation target record

    if id == None:
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
        conn.close()
        return render_template ('index.html')
    else:
        id = regd_id[-1]
    