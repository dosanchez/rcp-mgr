import mysql.connector
from crypt import methods
from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
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
    id = IntegerField ('Reg.No.')
    qty_um = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_symb = StringField('Unit of measurement', validators=[DataRequired(),Length(max=8)], 
        render_kw={"placeholder": "Unit of measure"})
    qty_base = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_un_t = SelectField('UM Type', validators=[AnyOf(values=['g','ml'])], 
        choices=['g','ml'])
    nav = SelectField('UM Type', validators=[AnyOf(values=[-1,0,1])], )

#view funtions
@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/templates/unitmeas.html', methods=['GET','POST'])
def unitmeas():


    form = Unitmeas()
    if form.validate_on_submit():

        sql = "SELECT COUNT(uni_symb) AS existe FROM unitmeas WHERE uni_symb = %s"
        param = form.uni_symb.data
        db.execute(sql, param)
        if  db.fetchall().get('existe') = 1:
            #update existing record

        else:
            #add new record
            sql = """INSERT INTO unitmeas (uni_symb, uni_conv, uni_un_t) 
                        VALUES (%s, %s, %s)"""
            params = (form.uni_symb.data, form.qty_base.data / form.qty_um.data,
                            form.uni_un_t.data)
            db.execute(sql, params)
            conn.commit()
            form.uni_symb.data = '' #clears form field
            print('agregué record')    
            print('redirigí')
            return redirect(url_for('unitmeas'))# clears POST data 


    #visualize registered units of measurement
    sql = "Select * from unitmeas"
    db.execute(sql)
    records = db.fetchall()
    column_names = db.column_names
    print('imprimí reg unit of measures')


    return render_template ('unitmeas.html', form=form, records=records,
                                                    column_names=column_names)


if __name__ == '__main__':
    app.run(debug=True)