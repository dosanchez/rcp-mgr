from typing import Type
import mysql.connector
from crypt import methods
from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField, HiddenField
from wtforms.validators import DataRequired, AnyOf, Length, NumberRange
from data import DataHandler as dth

#database connection
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                              host='192.168.100.254',
                              database='std')
# conn = mysql.connector.connect(user='root', password='Ds002011!!',
#                               host='200.125.169.75',
#                               database='std')
db = conn.cursor(dictionary=True, buffered=True)

#initialization
app=Flask(__name__)
app.config['SECRET_KEY']="place a key here"


#forms
class Unitmeas(FlaskForm):
    id = HiddenField()
    qty_um = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_symb = StringField('Unit of measurement', validators=[DataRequired(),Length(max=8)], 
        render_kw={"placeholder": "Unit of measurement"})
    qty_base = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_un_t = SelectField('UM Type', validators=[AnyOf(values=['g','ml'])], 
        choices=['g','ml'])

#view funtions
@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/templates/unitmeas.html', methods=['GET','POST'])
def unitmeas():
    form = Unitmeas()
    nav_button =  request.form.get('nav') #saves form navigation data
    try:
        nav_button = int(nav_button)
    except:
        pass
    

    if form.validate_on_submit():
        uni_conv = form.qty_base.data / form.qty_um.data
        record = dth.from_dict2sql(conn, {
                                        'unitmeas':[{
                                            'id':int(form.id.data),
                                            'uni_conv':uni_conv,
                                            'uni_un_t':form.uni_un_t.data,
                                            'uni_symb':form.uni_symb.data 
                                                    }]
                                        }
        )

        if nav_button == None: #not a nav post
            
            existe = dth.from_dict2sql(conn, {
                                        'unitmeas':[{
                                            'uni_symb':form.uni_symb.data
                                                    }]
                                        }
            ) #creates instance to chk if record exist
            if  existe.chk_sgl_fld():   #chk if record exists
                
                #update existing record
                record.update()
                return redirect(url_for('unitmeas'))# clears POST data

            else:
                
                record.add_new()
                return redirect(url_for('unitmeas'))# clears POST data 


    #visualize registered U.M and moves form to nav target
    
    sql = """Select id, uni_symb AS 'Unit of Measurement', 
                    uni_conv AS 'Qty', uni_un_t AS 'UM type' 
             from unitmeas"""
    db.execute(sql)
    records = db.fetchall()
    column_names = db.column_names

    regd_id =[row.get('id') for row in records] #making a list of registered ids
    last_index = len(regd_id) -1 #calc id list length
    id = form.id.data
    
    #resolve id value of the target record

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
    else:
        id = regd_id[-1]

    #visualize the target record
    sql = "SELECT * FROM unitmeas WHERE id = %s"
    db.execute(sql, (id,))
    tgt_record = db.fetchone()
    form.qty_um.data = 1
    form.uni_symb.data = session['uni_symb'] = tgt_record.get('uni_symb')
    form.qty_base.data = session['uni_conv'] = tgt_record.get('uni_conv')
    form.uni_un_t.data = session['uni_un_t'] = tgt_record.get('uni_un_t')
    form.id.data = session['id'] = tgt_record.get('id')
    tgt_record = db.fetchall()
    print (session['uni_symb'])

    return render_template ('unitmeas.html', form = form, records = records,
                            column_names = column_names)


if __name__ == '__main__':
    app.run(debug=True)
