from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, HiddenField, BooleanField 
from wtforms import Form, FormField, IntegerField, DateField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange,InputRequired
from wtforms.validators import Optional

class Recet_de(Form):
    """wtform for recipe form details"""
    idx = HiddenField()
    rcd_enca = HiddenField()
    rcd_ing = SelectField('Ingredient', validators=[DataRequired()], coerce= int)
    rcd_qty = FloatField('Qty',validators=[DataRequired(), NumberRange(min = 0)],
                            default = 1)
    rcd_unit = SelectField('Unit of measure', validators=[DataRequired()],
                            coerce = int)
    rcd_yiel = FloatField('Ingredient yield', validators=[DataRequired(),
                            NumberRange(min = 0)],default = 0.98)
class Rcv_de(Form):
    """wtform for receive form details"""
    idx = HiddenField()
    log_enca = HiddenField()
    log_sku = SelectField('Sku', validators=[DataRequired()], coerce= int)
    log_qty = FloatField('Qty',validators=[DataRequired(),
                            NumberRange(min = 0)], default = 1)
    log_pric = FloatField('Unit Price',validators=[DataRequired(),
                            NumberRange(min = 0)], default = 0.1)
    log_tax = FloatField('Tax amount', default = 0,
                            validators=[NumberRange(min = 0, max = 1)])
    log_alm = SelectField('Receiving warehouse', coerce= int)

class Unitmeas(FlaskForm):
    """wtform for Units of measure"""
    id = HiddenField()
    qty_um = FloatField('Qty',validators=[DataRequired(), 
                            NumberRange(min=0.001)], 
                            render_kw={"placeholder": "qty"}, default = 1)
    uni_symb = StringField('Unit of measurement', validators=[DataRequired(),
                            Length(max=8)], 
                            render_kw={"placeholder": "Unit of measurement"})
    qty_base = FloatField('Qty',validators=[DataRequired(), 
                            NumberRange(min=0.001)], 
                            render_kw={"placeholder": "qty"}, default = 1)
    uni_un_t = SelectField('UM Type', validators=[DataRequired()], 
                            choices=['g','ml'], default = 'g')
    uni_ebld = BooleanField('Enabled', default = "checked", false_values=('',False,'false',))

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
    rct_cost = FloatField('Actual Cost', render_kw = {'disabled':''}, default = 0)
    rct_cosc = FloatField('Standard Cost', render_kw = {'disabled':''}, default = 0)
    rct_dens = FloatField('Ingredient density',validators=[DataRequired()], 
                            render_kw={"placeholder": "Density"}, default = 1)
    rct_denu = SelectField('Density UM', validators=[DataRequired()], 
                            choices=['g/ml','g/unit'], default ='g/ml')
    rct_ebld = BooleanField('Enabled', default = True, false_values=('',))

class Recet_en(FlaskForm):
    """wtform for recipe form header"""
    id = HiddenField()
    rct_name = StringField('Recipe/Plate Name', validators=[DataRequired(),
                            Length(max=16)], 
                            render_kw={"placeholder": "e.g. French Fries Side"})
    rct_cost = FloatField('Actual Cost', render_kw = {'disabled':''}, default = 0)
    rct_cosc = FloatField('Standard Cost', render_kw = {'disabled':''}, default = 0)
    rct_dens = FloatField('Recipe/Plate density',validators=[DataRequired()], 
                            render_kw={"placeholder": "density"}, default = 1)
    rct_denu = SelectField('Recipe/Plate density UM', validators=[DataRequired()], 
                            choices=['g/ml','g/unit'], default ='g/unit')
    rct_yiel = FloatField('Recipe yield',validators=[DataRequired()], 
                            render_kw={"placeholder": "e.g. 0.98"}, default = 0.95)
    rct_serv = FloatField('Servings',validators=[DataRequired()], 
                            render_kw={"placeholder": "e.g. 0.98"}, default = 1)
    rct_unit = SelectField('serv UM', validators=[DataRequired()], coerce = int)
    rct_ebld = BooleanField('Enabled', default = "checked", false_values=('',))
    subform = FormField(Recet_de)


class Socio(FlaskForm):
    """wtform for Business partners (clients and vendors)"""
    id = HiddenField()
    soc_name = StringField('Business Partner', validators=[DataRequired(),
                            Length(max=32)], 
                            render_kw={"placeholder": "e.g. Ohio Steel Co."})
    soc_come= StringField('Reg. Name', validators=[Optional(), Length(max = 16)], 
                            render_kw={"placeholder": "reg, fiscal name"})
    soc_rnc = IntegerField('Fiscal No.', render_kw={"placeholder": "e.g. 101583983"}, 
                            validators=[Optional(), NumberRange(max = 9999999999999)])
    soc_ebld = BooleanField('Enabled', default = "checked")
    soc_cont = StringField('Contact', validators=[Length(max = 16)], 
                            render_kw={"placeholder": "e.g. Mr. James Watt"})   
    soc_addr = StringField('Business address', validators=[Length(max = 128)], 
                            render_kw={"placeholder": "up to 128 Chr. long"})
    soc_tel1 = StringField('Tel. 1', validators=[Optional(), Length(max=20)],
                            render_kw={"placeholder": "e.g. (212) 555-1332"})
    soc_tel2 = StringField('Tel. 2', validators=[Optional(), Length(max=20)],
                            render_kw={"placeholder": "e.g. (212) 555-1332"})
    soc_tel3 = StringField('Tel. 3', validators=[Optional(), Length(max=20)],
                            render_kw={"placeholder": "e.g. (212) 555-1332"})
    soc_wtax = BooleanField('Enabled', default = "checked")
    
class Sku(FlaskForm):
    id = HiddenField()
    sku_name = StringField('SKU Name', validators=[DataRequired(),
                            Length(max=16)], 
                            render_kw={"placeholder": "e.g. Heinz Tomato Soup"})
    sku_ingr = SelectField('Rel Recipe/ingr', coerce=int) 
    sku_cont = FloatField('Label weight',validators=[NumberRange(min = 0), 
                            InputRequired()], default=0)
    sku_unit = SelectField('Unit of measure', validators=[InputRequired()], 
                            coerce = int)
    sku_barc = StringField('Barcode', validators = [Length(max=16)],
                            render_kw={"placeholder": "insert barcode here"})
    sku_foto = FileField('Update SKU Picture',
                            validators = [FileAllowed(['jpg', 'png', 'jpeg'])])
    sku_pref = SelectField('Preferred Vendor', default = 0, coerce=int, 
                            validators=[Optional()])
    sku_itbi = FloatField('Sales Tax',validators=[DataRequired(), 
                            NumberRange(min=0, max=0.18)], default = 0.18)
    sku_vaci = FloatField('Empty container weight',validators=[InputRequired(), 
                            NumberRange(min = 0)])
    sku_v_unit = SelectField('Unit of measure',validators=[InputRequired()],
                            coerce = int)
    sku_ebld = BooleanField('Enabled', default = "checked")

class Rcv_en(FlaskForm):
    id = HiddenField()
    lox_vend = SelectField('Vendor',validators=[InputRequired()],coerce= int)
    lox_date = DateField('Reception Date', validators=[DataRequired()])
    lox_doc_no = IntegerField('Vendor Receipt No.', validators=[Optional()],
                            render_kw={"placeholder": "if other than rcpt tax No."})
    lox_datd = DateField('Reception Doc Date', validators=[DataRequired()])
    lox_nifn = StringField('receipt tax number',validators = [Optional(), Length(max=16)],
                            render_kw={"placeholder": "optional"})
    lox_sub = FloatField('Sub Total', default = 0,
                            validators=[NumberRange(min = 0)])
    lox_desc = FloatField('Discount',validators=[NumberRange(max = 0)], 
                            default = 0)
    lox_tax = FloatField('Total Tax',validators=[NumberRange(min = 0)], 
                            default = 0)
    subform = FormField(Rcv_de)
