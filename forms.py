from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange

class Unitmeas(FlaskForm):
    """wtform for Units of measure"""
    id = HiddenField()
    qty_um = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_symb = StringField('Unit of measurement', validators=[DataRequired(),Length(max=8)], 
        render_kw={"placeholder": "Unit of measurement"})
    qty_base = DecimalField('Qty',validators=[DataRequired(), NumberRange(min=0.001)], 
        render_kw={"placeholder": "qty"}, default = 1)
    uni_un_t = SelectField('UM Type', validators=[DataRequired()], 
        choices=['g','ml'], default = 'g')
    uni_ebld = BooleanField('Enabled', default = True, false_values=('',))

class Almacen(FlaskForm):
    """wtform for Warehouses"""
    id = HiddenField()
    alm_name = StringField('Warehouse', validators=[DataRequired(),Length(max=16)], 
        render_kw={"placeholder": "e.g. Branch 01"})
    alm_ebld = BooleanField('Enabled', default = True, false_values=('',))

class Ingredient(FlaskForm):
    """wtform for Ingredients"""
    id = HiddenField()
    ing_name = StringField('Ingredient', validators=[DataRequired(),Length(max=16)], 
        render_kw={"placeholder": "e.g. Paprika"})
    ing_unit = SelectField('Common unit of measurement', validators=[DataRequired()], 
        default = 'g')
    ing_dens = DecimalField('Ingredient density',validators=[DataRequired()], 
        render_kw={"placeholder": "Density"}, default = 1)
    ing_denu = SelectField('Density UM', validators=[DataRequired()], 
        choices=['g/ml','g/unit'], default ='g/ml')
    ing_rece = BooleanField('Recipe', default = False, false_values=('',), render_kw = {'disabled':''})
    ing_ebld = BooleanField('Enabled', default = True, false_values=('',))