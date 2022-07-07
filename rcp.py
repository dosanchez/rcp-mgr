import mysql.connector
from crypt import methods
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, AnyOf, Length, NumberRange


#database connection
#'kX0/_9@whS'
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                              host='192.168.100.254',
                              database='std')
db = conn.cursor()

#initialization
app=Flask(__name__)
app.config['SECRET_KEY']="place a key here"

#forms
class Unitmeas(FlaskForm):
    id = IntegerField ('Reg.No.')
    qty_um = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)])
    uni_symb = StringField('Unit of measure', validators=[DataRequired(),Length(max=8)], render_kw={"placeholder": "Unit of measure"})
    qty_base = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)])
    uni_un_t = SelectField('UM Type', validators=[AnyOf(values=['g','ml'])], choices=['g','ml'])
    #nav = SelectField('UM Type', validators=[AnyOf(values=[-1,0,1])], )


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
        val_qty_um=form.qty_um.data
        val_uni_symb = form.uni_symb.data
        val_qty_base = form.qty_base.data
        val_uni_un_t=form.uni_un_t.data
        form.qty_um.data = ''
        form.uni_symb.data = ''
        form.qty_base.data = ''
        form.uni_un_t.data = 'g'
        #form.nav.data = 0
        print (val_uni_symb, val_qty_base, val_qty_um)
        db.execute("INSERT INTO unitmeas (uni_symb, uni_conv, uni_un_t) VALUES (val_uni_symb , 29 / 1, 'g')")
        conn.commit()
        
        list = db.execute("SELECT * FROM unitmeas")

    print (list)

    return render_template ('unitmeas.html', form=form, list=list )


if __name__ == '__main__':
    app.run(debug=True)