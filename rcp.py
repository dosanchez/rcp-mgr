import mysql.connector
from crypt import methods
from flask import Flask, render_template
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
    uni_symb = StringField('Unit of measure', validators=[DataRequired(),Length(max=8)], 
        render_kw={"placeholder": "Unit of measure"})
    qty_base = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_un_t = SelectField('UM Type', validators=[AnyOf(values=['g','ml'])], 
        choices=['g','ml'])
    #nav = SelectField('UM Type', validators=[AnyOf(values=[-1,0,1])], )

#view funtions
@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/templates/unitmeas.html', methods=['GET','POST'])
def unitmeas():
    qty_um = None
    uni_symb = None
    qty_base = None
    uni_un_t = None
    #nav = None

    form = Unitmeas()
    if form.validate_on_submit():

        uni_symb=form.uni_symb.data
        uni_un_t=form.uni_un_t.data
        uni_conv = form.qty_base.data / form.qty_um.data
        form.qty_um.data = ''
        form.uni_symb.data = ''
        form.qty_base.data = ''
        form.uni_un_t.data = ''

        #add record
        sql = """INSERT INTO unitmeas (uni_symb, uni_conv, uni_un_t) 
                VALUES (%s, %s, %s)"""
        params = (uni_symb, uni_conv, uni_un_t)
        db.execute(sql, params)
        conn.commit()

    #visualize registered units of measure
    sql = "Select * from unitmeas"
    db.execute(sql)
    records = db.fetchall()
    column_names = db.column_names

    for row in records:
        for value in row.values():
            print (value)
    
    for header in column_names:
        if header == 'id':
            continue
        else:
            print(header)


    return render_template ('unitmeas.html', form=form, records=records, column_names=column_names)


if __name__ == '__main__':
    app.run(debug=True)