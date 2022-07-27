import mysql.connector
from flask import Flask, flash, render_template, request, session, redirect, url_for
from data import DataHandler as dth
from nav import navigate_to
from forms import Unitmeas, Almacen


#database connection
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                              host='192.168.100.254',
                              database='std')
# conn = mysql.connector.connect(user='root', password='Ds002011!!',
#                               host='200.125.169.75',
#                               database='std')
db = conn.cursor(dictionary=True, buffered=True)

#Flask initialization
app=Flask(__name__)
app.config['SECRET_KEY']="place a key here"


#view funtions
@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/templates/unitmeas.html', methods=['GET','POST'])
def unitmeas():
    form = Unitmeas()
    sqltable = 'unitmeas'
    nav_button =  request.form.get('nav') #saves form navigation request
    try:
        nav_button = int(nav_button)
    except:
        pass
    

    if form.validate_on_submit():
        uni_conv = form.qty_base.data / form.qty_um.data
        record = dth.from_dict2sql(conn, {
                                        sqltable:[{
                                            'id':int(form.id.data),
                                            'uni_conv':uni_conv,
                                            'uni_un_t':form.uni_un_t.data,
                                            'uni_symb':form.uni_symb.data,
                                            'uni_ebld':form.uni_ebld.data 
                                                    }]
                                        })

        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist
            existe = dth.from_dict2sql(conn, {
                                        sqltable:[{
                                            'uni_symb':form.uni_symb.data
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('unitmeas'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('unitmeas'))# clears POST data 


    records = navigate_to(nav_button, db, form, sqltable)
    column_names =['', 'Ud. base', 'Qty', 'Unit of measurement', 'Enabled']
    for row in records:
        print(row['uni_ebld'])

    return render_template ('unitmeas.html', form = form, records = records,
                            column_names = column_names)


@app.route('/templates/almacen.html', methods=['GET','POST'])
def almacen():
    form = Almacen()
    sqltable = 'almacen'
    nav_button =  request.form.get('nav') #saves form navigation request
    try:
        nav_button = int(nav_button)
    except:
        pass
    

    if form.validate_on_submit():

        record = dth.from_dict2sql(conn, {
                                        sqltable:[{
                                            'id':int(form.id.data),
                                            'alm_name':form.alm_name.data
                                                    }]
                                        })

        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist
            existe = dth.from_dict2sql(conn, {
                                        sqltable:[{
                                            'alm_name':form.alm_name.data
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('almacen'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('almacen'))# clears POST data 


    records = navigate_to(nav_button, db, form, sqltable)
    column_names =['', 'Warehouse', 'Enabled']

    return render_template ('almacen.html', form = form, records = records,
                            column_names = column_names)

if __name__ == '__main__':
    app.run(debug=True)
