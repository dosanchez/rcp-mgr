from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, AnyOf, Length, NumberRange

#initialization
app=Flask(__name__)
app.config['SECRET_KEY']="place a key here"

#forms
class Unitmeas(FlaskForm):
    id = IntegerField ('Reg.No.')
    qty_um = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)])
    uni_symb = StringField('Unit of measure', validators=[DataRequired(),Length(max=8)])
    qty_base = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)])
    uni_un_t = SelectField('UM Type', validators=[AnyOf(values=['g','ml'])])



@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/templates/unitmeas.html')
def unitmeas():
    return render_template ('unitmeas.html')


if __name__ == '__main__':
    app.run(debug=True)