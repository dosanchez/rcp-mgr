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
        render_kw={"placeholder": "Unit of measure"})
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
    if form.validate_on_submit():

        sql = "SELECT COUNT(uni_symb) AS existe FROM unitmeas WHERE uni_symb = %s"
        db.execute(sql,(form.uni_symb.data,))
        record = db.fetchone()
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
            return redirect(url_for('unitmeas'))# clears POST data

        else:
            #add new record
            sql = """INSERT INTO unitmeas (uni_symb, uni_conv, uni_un_t) 
                        VALUES (%s, %s, %s)"""
            params = (form.uni_symb.data, form.qty_base.data / form.qty_um.data,
                            form.uni_un_t.data)
            db.execute(sql, params)
            conn.commit()
            form.uni_symb.data = '' #clears form field
            return redirect(url_for('unitmeas'))# clears POST data 


    #visualize registered U.M and moves form to nav target
    sql = "Select * from unitmeas"
    db.execute(sql)
    records = db.fetchall()
    column_names = db.column_names

    regd_id =[row.get('id') for row in records] #making a list of ids
    num_regd_id = len(regd_id) #calc id list lenght
    
  
    print(session['id'])
    if form.id.data == None:
         form.id.data = regd_id[num_regd_id -1]
    elif request.form.get('nav') == "first":
        form.id.data = regd_id[0] 
    elif request.form.get('nav') == "last":
        form.id.data = regd_id[num_regd_id-1]
    elif request.form.get('nav') == "back" and regd_id.index(form.id.data) > 0:
        form.id.data = regd_id[regd_id.index(form.id.data)-1]
    elif request.form.get('nav') == "back" and regd_id.index(form.id.data) == 0:
        form.id.data = regd_id[0]
    elif request.form.get('nav') == "next" and regd_id.index(form.id.data) < (len(regd_id) - 1):
        form.id.data = regd_id[regd_id.index(form.id.data)+1]
    elif request.form.get('nav') == "next" and regd_id.index(form.id.data) == (len(regd_id) - 1):
        form.id.data = regd_id[num_regd_id-1]
    else:
        form.id.data =regd_id[num_regd_id-1]

    #visualize the target record
    sql = "SELECT * FROM unitmeas WHERE id = %s"
    db.execute(sql, (form.id.data,))
    tgt_record = db.fetchone()
    form.qty_um.data = 1
    form.uni_symb.data = tgt_record.get('uni_symb')
    form.qty_base.data = tgt_record.get('uni_conv')
    form.uni_un_t.data = tgt_record.get('uni_un_t')

    return render_template ('unitmeas.html', form=form, records=records,
                            column_names=column_names)


if __name__ == '__main__':
    app.run(debug=True)
