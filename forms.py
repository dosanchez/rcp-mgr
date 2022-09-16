from unicodedata import decimal
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, DecimalField, HiddenField, BooleanField 
from wtforms import Form, FormField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired


class Recet_de(Form):
    """wtform for recipe form details"""
    idx = HiddenField()
    rcd_enca = HiddenField()
    rcd_ing = SelectField('Ingredient', validators=[DataRequired()], coerce= int)
    rcd_qty = DecimalField('Qty',validators=[DataRequired()],
                            default = 1)
    rcd_unit = SelectField('Unit of measure', validators=[DataRequired()], coerce = int)
    rcd_yiel = DecimalField('Ingredient yield', validators=[DataRequired()],
                            default = 0.98)
    
class Unitmeas(FlaskForm):
    """wtform for Units of measure"""
    id = HiddenField()
    qty_um = DecimalField('Qty',validators=[DataRequired(), 
                            NumberRange(min=0.001)], 
                            render_kw={"placeholder": "qty"}, default = 1)
    uni_symb = StringField('Unit of measurement', validators=[DataRequired(),
                            Length(max=8)], 
                            render_kw={"placeholder": "Unit of measurement"})
    qty_base = DecimalField('Qty',validators=[DataRequired(), 
                            NumberRange(min=0.001)], 
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
    rct_name = StringField('Ingredient', validators=[DataRequired(),
                            Length(max=16)], 
                            render_kw={"placeholder": "e.g. Paprika"})
    rct_cost = DecimalField('Actual Cost', render_kw = {'disabled':''}, default = 0)
    rct_cosc = DecimalField('Standard Cost', render_kw = {'disabled':''}, default = 0)
    #rct_unit = SelectField('Common UM', validators=[DataRequired()], coerce = int)
    rct_dens = DecimalField('Ingredient density',validators=[DataRequired()], 
                            render_kw={"placeholder": "Density"}, default = 1)
    rct_denu = SelectField('Density UM', validators=[DataRequired()], 
                            choices=['g/ml','g/unit'], default ='g/ml')
    rct_yiel = DecimalField('Ingredient yield',validators=[DataRequired()], 
                            render_kw={"placeholder": "e.g. 0.98"}, default = 1)
    rct_ebld = BooleanField('Enabled', default = True, false_values=('',))

class Recet_en(FlaskForm):
    """wtform for recipe form header"""
    id = HiddenField()
    rct_name = StringField('Recipe/Plate Name', validators=[DataRequired(),
                            Length(max=16)], 
                            render_kw={"placeholder": "e.g. French Fries Side"})
    rct_cost = DecimalField('Actual Cost', render_kw = {'disabled':''}, default = 0)
    rct_cosc = DecimalField('Standard Cost', render_kw = {'disabled':''}, default = 0)
    rct_dens = DecimalField('Recipe/Plate density',validators=[DataRequired()], 
                            render_kw={"placeholder": "density"}, default = 1)
    rct_denu = SelectField('Recipe/Plate density UM', validators=[DataRequired()], 
                            choices=['g/ml','g/unit'], default ='g/unit')
    rct_yiel = DecimalField('Recipe yield',validators=[DataRequired()], 
                            render_kw={"placeholder": "e.g. 0.98"}, default = 1)
    rct_unit = SelectField('Common UM', validators=[DataRequired()], coerce = int)
    rct_ebld = BooleanField('Enabled', default = "checked", false_values=('',))
    subform = FormField(Recet_de)


class Socio(FlaskForm):
    """wtform for Business partners (clients and vendors)"""
    id = HiddenField()
    soc_name = StringField('Business Partner', validators=[DataRequired(),
                            Length(max=32)], 
                            render_kw={"placeholder": "e.g. Ohio Steel Co."})
    soc_come= StringField('Reg. Name', validators=[Length(max = 16)], 
                            render_kw={"placeholder": "reg, fiscal name"})
    soc_rnc = IntegerField('Fiscal No.', validators=[NumberRange(max = 9999999999999)],
                            render_kw={"placeholder": "e.g. 101583983"})
    soc_ebld = BooleanField('Enabled', default = "checked", false_values=('',))
    soc_cont = StringField('Contact', validators=[Length(max = 16)], 
                            render_kw={"placeholder": "e.g. Mr. James Watt"})   
    soc_addr = StringField('Business Partner', validators=[Length(max = 128)], 
                            render_kw={"placeholder": "up to 64 Chr. long"})
    soc_tel1 = IntegerField('Tel. 1', validators=[NumberRange(max = 9999999999999, message='if no number enter 0')],
                            render_kw={"placeholder": "e.g. 12125551332"})
    soc_tel2 = IntegerField('Tel. 1', validators=[NumberRange(max = 9999999999999)],
                            render_kw={"placeholder": "e.g. 12125551332"})
    soc_tel3 = IntegerField('Tel. 1', validators=[NumberRange(max = 9999999999999)],
                            render_kw={"placeholder": "e.g. 12125551332"})
    
class Sku(FlaskForm):
    id = HiddenField()
    sku_name = StringField('SKU Name', validators=[DataRequired(),
                            Length(max=16)], 
                            render_kw={"placeholder": "e.g. Heinz Tomato Soup"})
    sku_ingr = SelectField('Rel Recipe/ingr', default = None, coerce= int) 
    sku_cont = DecimalField('Label weight',validators=[NumberRange(min = 0)], default = 0)
    sku_unit = SelectField('Unit of measure', validators=[DataRequired()], 
                            coerce = int)
    sku_barc = StringField('Barcode', validators = [Length(max=16)], 
                            render_kw={"placeholder": "insert barcode here"})
    sku_foto = FileField('Update SKU Picture', validators = [FileAllowed(['jpg', 'png'])])
    sku_pref = SelectField('Preferred Vendor', default = '', coerce= int)
    sku_itbi = DecimalField('Sales Tax',validators=[NumberRange(min = 0)], default = 0.18)
    sku_vaci = DecimalField('Empty container weight',validators=[NumberRange(min = 0)])
        
    sku_v_unit = SelectField('Unit of measure', default = ('','---'), coerce = int)
    sku_ebld = BooleanField('Enabled', default = "checked", false_values=('',))

