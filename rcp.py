import mysql.connector
from flask import Flask, render_template, session, request, redirect, url_for
from data import DataHandler as dth, select as sel
from nav import navigate_to
from forms import Ingredient, Unitmeas, Almacen, Recet_en


#database connection
conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
                              host='192.168.100.254',
                              database='std')
# conn = mysql.connector.connect(user='rcp', password='kX0/_9@whS',
#                               host='200.125.169.75',
#                               database='std')
db = conn.cursor(dictionary=True, buffered=True)

# database parent-child table


#Flask initialization
app=Flask(__name__)
app.config['SECRET_KEY']="place a key here"


#view funtions
@app.route('/', methods=['GET','POST'])
def index():

    return render_template ('index.html')

@app.route('/templates/unitmeas.html', methods=['GET','POST'])
def unitmeas():
    form = Unitmeas()
    table_list = ['unitmeas']
    nav_button =  request.form.get('nav') #saves form navigation request
    try:
        nav_button = int(nav_button)
    except:
        pass
    

    if form.validate_on_submit():
        uni_conv = form.qty_base.data / form.qty_um.data
        record = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data,
                                            'uni_conv':uni_conv,
                                            'uni_un_t':form.uni_un_t.data,
                                            'uni_symb':form.uni_symb.data,
                                            'uni_ebld':form.uni_ebld.data 
                                                    }]
                                        })

        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist
            existe = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'uni_symb':form.uni_symb.data
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('unitmeas'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('unitmeas'))# clears POST data 


    records, relation = navigate_to(nav_button, db, form, table_list)
    column_names =[['Registered unit of measurement', ['', 'Ud. base', 'Qty', 'Unit of measurement', 'Enabled']]]

    return render_template ('unitmeas.html', form = form, records = records,
                            column_names = column_names)


@app.route('/templates/almacen.html', methods=['GET','POST'])
def almacen():
    form = Almacen()
    table_list = ['almacen']

    nav_button =  request.form.get('nav') #saves form navigation request
    try:
        nav_button = int(nav_button)
    except:
        pass
    

    if form.validate_on_submit():

        record = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data,
                                            'alm_name':form.alm_name.data,
                                            'alm_ebld':form.alm_ebld.data
                                                    }]
                                        })

        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist
            existe = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'alm_name':form.alm_name.data
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('almacen'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('almacen'))# clears POST data 


    records, relation = navigate_to(nav_button, db, form, table_list)
    column_names =[['Registered Warehouses',['', 'Warehouse', 'Enabled']]]

    return render_template ('almacen.html', form = form, records = records,
                            column_names = column_names)


@app.route('/templates/ingredient.html', methods=['GET','POST'])
def ingredient():
    form = Ingredient()
    table_list = ['ingredient']
    
    form.ing_unit.choices = sel.UM_ebld(db) #Queries for Selectfields active choices
    ing_unit_choices = sel.UM_all(db) #Queries for all Selectfields choices

        
    nav_button =  request.form.get('nav') #saves form navigation request
    try:
        nav_button = int(nav_button)
    except:
        pass
    

    if form.validate_on_submit():
        #Selectfield values

        record = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data,
                                            'ing_name':form.ing_name.data,
                                            'ing_unit':form.ing_unit.data,
                                            'ing_dens':form.ing_dens.data,
                                            'ing_denu':form.ing_denu.data,
                                            'ing_rece':form.ing_rece.data,
                                            'ing_ebld':form.ing_ebld.data  
                                                    }]
                                        })

        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist
            existe = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('ingredient'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('ingredient'))# clears POST data 


    records, relation = navigate_to(nav_button, db, form, table_list)
    column_names =[['Registered Ingredients',['', 'Ingredient', 'Common UM', 'Density', 'Densi UM',
                     'Recipe','Enabled']]]

    return render_template ('ingredient.html', form = form, records = records,
                            column_names = column_names, ing_unit_choices = ing_unit_choices)

@app.route('/templates/recipe.html', methods=['GET','POST'])
def recipe():
    form = Recet_en()
    table_list = ['recet_en', 'recet_de']
    
    #Queries for Selectfields active choices
    form.rct_unit.choices = form.subform.rcd_unit.choices = sel.UM_ebld(db)
    form.subform.rcd_ing.choices = sel.ingred_ebld(db)

    #Queries for all possible Selectfields choices
    rcd_unit_choices = rct_unit_choices = sel.UM_all(db)
    rcd_ing_choices = sel.ingred_all(db)

    nav_button =  request.form.get('nav') #saves form navigation request
    try:
        nav_button = int(nav_button)
    except:
        pass
    
    print(nav_button)
    print(form.validate_on_submit())

    if form.validate_on_submit():


        #Selectfield values
        listsql = listsql2 = {
                                table_list[0]:[{
                                    'id':form.id.data,
                                    'rct_name':form.rct_name.data,
                                    'rct_cost':form.rct_cost.data,
                                    'rct_cosc':form.rct_cosc.data,
                                    'rct_unit':form.rct_unit.data,
                                    'rct_dens':form.rct_dens.data,
                                    'rct_denu':form.rct_denu.data,
                                    'rct_yiel':form.rct_yiel.data,
                                    'rct_ebld':form.rct_ebld.data  
                                            }],
                                table_list[1]:[{
                                    'id':form.subform.idx.data,
                                    'rcd_enca':form.subform.rcd_enca.data,
                                    'rcd_ing':form.subform.rcd_ing.data,
                                    'rcd_qty':form.subform.rcd_qty.data,
                                    'rcd_unit':form.subform.rcd_unit.data,
                                    'rcd_yiel':form.subform.rcd_yiel.data  
                                            }]
                                
                                }
        listsql1 ={list(listsql.keys())[0]: list(listsql.values())[0]} 
        del listsql2 [list(listsql.keys())[0]]


        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist
            record = dth.from_dict2sql(conn, listsql1)
            existe = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data
                                                    }]
                                        }
            ) 
            
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('recipe'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('recipe'))# clears POST data 

        if nav_button == "submit1": #not a nav post
            #creates instance to chk if record exist
            record = dth.from_dict2sql(conn, listsql2)
            existe = dth.from_dict2sql(conn, {
                                        table_list[1]:[{
                                            'id':form.subform.idx.data
                                                    }]
                                        }
            ) 
            print (existe.chk_sgl_fld())
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('recipe'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('recipe'))# clears POST data

    records, relation = navigate_to(nav_button, db, form, table_list)
    records.pop(0) #form header records not needed
    column_names =[['Recipe ingredients',['', '', 'Ingredient', 'Qty', 'Unit of measure',
                     'Ingredient yield']]]
    rcd_len = len(records)

    return render_template ('recipe.html', form = form, records = records,
                            column_names = column_names, 
                            rcd_unit_choices = rcd_unit_choices ,
                            rct_unit_choices = rct_unit_choices,
                            rcd_ing_choices = rcd_ing_choices,
                            relation = relation,
                            rcd_len = rcd_len)

if __name__ == '__main__':
    app.run(debug=True)
