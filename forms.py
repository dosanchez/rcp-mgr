from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, HiddenField, BooleanField
from wtforms.validators import DataRequired, AnyOf, Length, NumberRange

class Unitmeas(FlaskForm):
    """wtform for Units of measure"""
    id = HiddenField()
    qty_um = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_symb = StringField('Unit of measurement', validators=[DataRequired(),Length(max=8)], 
        render_kw={"placeholder": "Unit of measurement"})
    qty_base = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_un_t = SelectField('UM Type', validators=[AnyOf(values=['g','ml'])], 
        choices=['g','ml'])
    uni_ebld = BooleanField('Enabled', default = True, false_values=('',))

class Almacen(FlaskForm):
    """wtform for Warehouses"""
    id = HiddenField()
    alm_name = StringField('Warehouse', validators=[DataRequired(),Length(max=16)], 
        render_kw={"placeholder": "e.g. Branch 01"})
    alm_ebld = BooleanField('Enabled', default = True, false_values=('',))
