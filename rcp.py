from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired, AnyOf, Length

#initialization
app=Flask(__name__)
app.config['SECRET_KEY']="vixxux"

#forms
class Unitmeas(FlaskForm):
    id = IntegerField ('Reg.No.')
    uni_un_t = SelectField('UM Type', validators=[AnyOf(values=['g','ml','unit'])])
    uni_conv = DecimalField('Equiv. qty',validators=[DataRequired()])
    uni_symb = StringField('name', validators=[DataRequired(),Length(max=8)])


@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/templates/unitmeas.html')
def unitmeas():
    return render_template ('index.html')


if __name__ == '__main__':
    app.run(debug=True)