import mysql.connector
from crypt import methods
from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField, HiddenField
from wtforms.validators import DataRequired, AnyOf, Length, NumberRange


#database connection
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                              host='192.168.100.254',
                              database='std')
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
    nav_button =  request.form.get('nav') #
    
    if form.validate_on_submit():
        print(form.qty_um.data, form.uni_symb.data, form.qty_base.data, form.uni_un_t.data)
        print('validé')

        sql = "SELECT COUNT(uni_symb) AS existe FROM unitmeas WHERE uni_symb = %s"
        db.execute(sql,(form.uni_symb.data,))
        record = db.fetchone()

        if nav_button == None:
            if  record.get('existe') == 1:
                #update existing record
                sql="""UPDATE unitmeas 
                        SET uni_conv = %s,
                            uni_un_t = %s
                        WHERE uni_symb = %s""" 
                params = (form.qty_base.data / form.qty_um.data, form.uni_un_t.data,
                            form.uni_symb.data)
                db.execute(sql, params)
                conn.commit()
                print(form.qty_um.data, form.uni_symb.data, form.qty_base.data, form.uni_un_t.data)
                print('mofifiqué')

                return redirect(url_for('unitmeas'))# clears POST data

            else:
                #add new record
                sql = """INSERT INTO unitmeas (uni_symb, uni_conv, uni_un_t) 
                            VALUES (%s, %s, %s)"""
                params = (form.uni_symb.data, form.qty_base.data / form.qty_um.data,
                                form.uni_un_t.data)
                db.execute(sql, params)
                conn.commit()
                
                print('agregué')
                return redirect(url_for('unitmeas'))# clears POST data 


    #visualize registered U.M and moves form to nav target
    
    sql = "Select * from unitmeas"
    db.execute(sql)
    records = db.fetchall()
    column_names = db.column_names
    print(form.qty_um.data, form.uni_symb.data, form.qty_base.data, form.uni_un_t.data)
    print('paso records y column_names')

    regd_id =[row.get('id') for row in records] #making a list of registered ids
    last_index = len(regd_id) -1 #calc id list length
    id = form.id.data
    print(form.qty_um.data, form.uni_symb.data, form.qty_base.data, form.uni_un_t.data)
    print('reviso la navegación')
    if id == None:
         id = regd_id[-1]
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
    form.uni_symb.data = tgt_record.get('uni_symb')
    form.qty_base.data = tgt_record.get('uni_conv')
    form.uni_un_t.data = tgt_record.get('uni_un_t')
    form.id.data = tgt_record.get('id')
    tgt_record = db.fetchall()
    print('visuaizo el target field')
    print(nav_button, form.qty_um.data, form.uni_symb.data, form.qty_base.data, form.uni_un_t.data, form.id.data)
    return render_template ('unitmeas.html', form = form, records = records,
                            column_names = column_names)


if __name__ == '__main__':
    app.run(debug=True)
