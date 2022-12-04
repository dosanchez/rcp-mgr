import datetime
import mysql.connector
from flask import Flask, render_template, session, request, redirect, url_for
from data import DataHandler as dth, select as sel, dlt, update, save_file
from nav import navigate_to
from forms import Ingredient, Sku, Unitmeas, Almacen, Recet_en, Socio, Rcv_en
import os

#database connection
conn = mysql.connector.connect(user='sql5514428', password='C3b4Xn6K4Z',
                              host='sql5.freesqldatabase.com',
                              database='sql5514428')

db = conn.cursor(dictionary=True, buffered=True)


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

    #if request.form.get('nav') in None --> its a redirect 
    #--> its either an update, new or deleted record hence not necesarilly 
    #last record should be displayed 
    if request.form.get('nav'):
        nav_button =  request.form.get('nav') #saves form navigation request
    else:
        nav_button = session.get('curr_rcd_' + type(form).__name__)

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
                                            'id':form.id.data
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('unitmeas'))# clears POST data

            else:
                #adds new record
                session['curr_rcd_' + type(form).__name__] = None 
                    # ^ so it navigates to the last record after adding
                record.add_new()
                return redirect(url_for('unitmeas'))# clears POST data 


    records, relation = navigate_to(nav_button, conn, form, table_list)
    column_names =[['Registered unit of measurement', ['', 'Ud. base', 'Qty', 'Unit of measurement', 'Enabled']]]

    return render_template ('unitmeas.html', form = form, records = records,
                            column_names = column_names)


@app.route('/templates/socio.html', methods=['GET','POST'])
def socio():
    form = Socio()
    table_list = ['socio']

    #if request.form.get('nav') in None --> its a redirect 
    #--> its either an update, new or deleted record hence not necesarilly 
    #last record should be displayed 
    if request.form.get('nav'):
        nav_button =  request.form.get('nav') #saves form navigation request
    else:
        nav_button = session.get('curr_rcd_' + type(form).__name__)
    try:
        nav_button = int(nav_button)
    except:
        pass
    
    if form.validate_on_submit():

        record = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data,
                                            'soc_name':form.soc_name.data,
                                            'soc_come':form.soc_come.data,
                                            'soc_rnc':form.soc_rnc.data,
                                            'soc_ebld':form.soc_ebld.data,
                                            'soc_cont ':form.soc_cont.data,
                                            'soc_addr':form.soc_addr.data,
                                            'soc_tel1':form.soc_tel1.data,
                                            'soc_tel2':form.soc_tel2.data,
                                            'soc_tel3':form.soc_tel3.data,
                                            'soc_wtax':form.soc_wtax.data
                                                    }]
                                        })

        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist
            existe = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data,
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('socio'))# clears POST data

            else:
                #adds new record
                session['curr_rcd_' + type(form).__name__] = None 
                    # ^ so it navigates to the last record after adding
                record.add_new()
                return redirect(url_for('socio'))# clears POST data 


    records, relation = navigate_to(nav_button, conn, form, table_list)
    column_names =[['Registered Business Partners',['id', 'Name', 'Fiscal Name',
                     'Tax No.', 'enabled', 'Contact', 'Adress', 'Tel. 1', 'Tel. 2',
                      'Tel. 3','Tax incld in prc']]]

    return render_template ('socio.html', form = form, records = records,
                            column_names = column_names)


@app.route('/templates/almacen.html', methods=['GET','POST'])
def almacen():
    form = Almacen()
    table_list = ['almacen']

    #if request.form.get('nav') in None --> its a redirect 
    #--> its either an update, new or deleted record hence not necesarilly 
    #last record should be displayed 
    if request.form.get('nav'):
        nav_button =  request.form.get('nav') #saves form navigation request
    else:
        nav_button = session.get('curr_rcd_' + type(form).__name__)

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
                                            'id':form.id.data
                                                    }]
                                        }
            ) 
            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('almacen'))# clears POST data

            else:
                #adds new record
                session['curr_rcd_' + type(form).__name__] = None 
                    # ^ so it navigates to the last record after adding
                record.add_new()
                return redirect(url_for('almacen'))# clears POST data 


    records, relation = navigate_to(nav_button, conn, form, table_list)
    column_names =[['Registered Warehouses',['', 'Warehouse', 'Enabled']]]

    return render_template ('almacen.html', form = form, records = records,
                            column_names = column_names)


@app.route('/templates/ingredient.html', methods=['GET','POST'])
def ingredient():
    form = Ingredient()
    table_list = ['recet_en']
        
    #if request.form.get('nav') in None --> its a redirect 
    #--> its either an update, new or deleted record hence not necesarilly 
    #last record should be displayed 
    if request.form.get('nav'):
        nav_button =  request.form.get('nav') #saves form navigation request
    else:
        nav_button = session.get('curr_rcd_' + type(form).__name__)

    try:
        nav_button = int(nav_button)
    except:
        pass
    
    if form.validate_on_submit():

        record = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data,
                                            'rct_name':form.rct_name.data,
                                            'rct_cost':form.rct_cost.data,
                                            'rct_cosc':form.rct_cosc.data,
                                            'rct_dens':form.rct_dens.data,
                                            'rct_denu':form.rct_denu.data,
                                            'rct_ebld':form.rct_ebld.data  
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
                session['curr_rcd_' + type(form).__name__] = None 
                    # ^ so it navigates to the last record after adding
                record.add_new(rct_rece = 0)
                return redirect(url_for('ingredient'))# clears POST data 


    records, relation = navigate_to(nav_button, conn, form, table_list)
    column_names =[['Registered Ingredients',['', 'Ingredient', 'Costo Real',
                    'Costo Std', 'Density', 'Densi UM', 'Enabled']]]
    
    return render_template ('ingredient.html', form = form, records = records,
                            column_names = column_names)


@app.route('/templates/recipe.html', methods=['GET','POST'])
def recipe():
    form = Recet_en()
    table_list = ['recet_en', 'recet_de']
    #Queries for Selectfields active choices
    form.rct_unit.choices = form.subform.rcd_unit.choices = sel.ebld_choices(db,
                                                    'unitmeas',
                                                    'uni_symb', 
                                                    'uni_ebld')
    form.subform.rcd_ing.choices = sel.ebld_choices(db, 'recet_en', 'rct_name',
                                                     'rct_ebld')
   
    #Queries for all possible Selectfields choices
    rcd_unit_choices = sel.all_choices(db, 'unitmeas', 'uni_symb')
    rcd_ing_choices = sel.all_choices(db, 'recet_en', 'rct_name')

    #if request.form.get('nav') is None --> its a redirect 
    #--> its either an update, new or deleted record hence not necesarilly 
    #last record should be displayed 
    if request.form.get('nav'):
        nav_button =  request.form.get('nav') #saves form navigation request
    else:
        nav_button = session.get('curr_rcd_' + type(form).__name__)

    session['sub_nav_button'] = request.form.get('subnav') #saves subform navigation request
    session['delete_id'] = request.form.get('delete')

    try:
        nav_button = int(nav_button)
    except:
        pass
    
    try:
        session['sub_nav_button'] = int(session['sub_nav_button'])
    except:
        pass

    try:
        session['delete_id'] = int(session['delete_id'])
    except:
        pass    

    print('formvalidate', form.validate_on_submit())
    if form.validate_on_submit():

        listsql = listsql2 = {
                                table_list[0]:[{
                                    'id':form.id.data,
                                    'rct_name':form.rct_name.data,
                                    'rct_cost':form.rct_cost.data,
                                    'rct_cosc':form.rct_cosc.data,
                                    'rct_dens':form.rct_dens.data,
                                    'rct_denu':form.rct_denu.data,
                                    'rct_yiel':form.rct_yiel.data,
                                    'rct_serv':form.rct_serv.data,
                                    'rct_unit':form.rct_unit.data,
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
                session['curr_rcd_' + type(form).__name__] = None 
                    # ^ so it navigates to the last record after adding
                record.add_new(rct_rece = 1)
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

            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                return redirect(url_for('recipe'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('recipe'))# clears POST data
        
        if session['delete_id']:
            dlt.id(conn, table_list[1], session['delete_id'])
            return redirect(url_for('recipe'))# clears POST data
           

    records, relation = navigate_to(nav_button, conn, form, table_list)
    session['relation'] = relation

    records.pop(0) #form header records not needed nav populates header

    column_names =[['Recipe ingredients',['', '', 'Ingredient', 'Qty', 'Unit of measure',
                     'Ingredient yield']]]
    rcd_len = len(records)

    return render_template ('recipe.html', form = form, records = records,
                            column_names = column_names, 
                            rcd_unit_choices = rcd_unit_choices ,
                            rcd_ing_choices = rcd_ing_choices,
                            relation = relation,
                            rcd_len = rcd_len)


@app.route('/templates/sku.html', methods=['GET','POST'])
def sku():
    # paths for files
    sku_pic_path = os.path.join(app.root_path,'static/skupics')
    session['sku_notimg'] = url_for('static',  filename = 'skupics/595ab936.jpg')
    form = Sku()
    table_list = ['sku']


    #Queries for Selectfields active choices
    form.sku_ingr.choices = sel.ebld_choices(db, 'recet_en', 'rct_name', 'rct_ebld', blank = True) 
    form.sku_unit.choices = form.sku_v_unit.choices = sel.ebld_choices(db,
                                                        'unitmeas','uni_symb',
                                                        'uni_ebld')
    form.sku_pref.choices = sel.ebld_choices(db, 'socio', 'soc_name', 'soc_ebld', blank = True)

    #Queries for all Selectfields choices
    sku_ingr_choices = sel.all_choices(db, 'recet_en', 'rct_name')
    sku_unit_choices = sel.all_choices(db, 'unitmeas', 'uni_symb')
    sku_pref_choices = sel.all_choices(db, 'socio', 'soc_name')

    #if request.form.get('nav') in None --> its a redirect 
    #--> its either an update, new or deleted record hence not necesarilly 
    #last record should be displayed 
    if request.form.get('nav'):
        nav_button =  request.form.get('nav') #saves form navigation request
    else:
        nav_button = session.get('curr_rcd_' + type(form).__name__)
    
    try:
        nav_button = int(nav_button)
    except:
        pass
    for error in form.sku_ingr.errors:
        print('skuing',error)
    print('validateonsubmit', form.validate_on_submit())

    for error in form.sku_cont.errors:
        print('skucont',error)
        
    if form.validate_on_submit():
        
        record = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data,
                                            'sku_name':form.sku_name.data,
                                            'sku_ingr':form.sku_ingr.data,
                                            'sku_cont':form.sku_cont.data,
                                            'sku_unit':form.sku_unit.data,
                                            'sku_barc':form.sku_barc.data,
                                            'sku_foto':form.sku_foto.data,
                                            'sku_pref':form.sku_pref.data,
                                            'sku_itbi':form.sku_itbi.data,
                                            'sku_vaci':form.sku_vaci.data,
                                            'sku_v_unit':form.sku_v_unit.data,
                                            'sku_ebld':form.sku_ebld.data  
                                                    }]
                                        })
        
        #checks for Selectfields where 0 is meant to be null
        if record.rcd.get(table_list[0])[0].get('sku_ingr') == 0:
            record.rcd[table_list[0]][0]['sku_ingr'] = None
        if record.rcd.get(table_list[0])[0].get('sku_pref') == 0:
            record.rcd[table_list[0]][0]['sku_pref'] = None
        
        if nav_button == "submit": #not a nav post
            #creates instance to chk if record exist

            existe = dth.from_dict2sql(conn, {
                                        table_list[0]:[{
                                            'id':form.id.data
                                                    }]
                                        }
            ) 

            #update current record instance sku_foto attribute to either 
            #to pic name in database or new pic name of loaded picture
            #so info in database stays updated
            img_rcd = sel.all(db, table_list[0], id = form.id.data)
            if  img_rcd:
                name = img_rcd[0].get('sku_foto')
            else:
                name = None

            if form.sku_foto.data:                 
                record.rcd.get(table_list[0])[0]['sku_foto']  = "\'" + save_file(form.sku_foto.data, 
                    sku_pic_path, f_name = name) + "\'" 
            else:
                if not name:
                    record.rcd.get(table_list[0])[0]['sku_foto'] = name
                else:
                    record.rcd.get(table_list[0])[0]['sku_foto'] = "\'" + name + "\'"


            if  existe.chk_sgl_fld():   #chk if record exists

                #update existing record
                record.update()
                return redirect(url_for('sku'))# clears POST data

            else:
                #adds new record
                session['curr_rcd_' + type(form).__name__] = None 
                    # ^ so it navigates to the last record after adding
                record.add_new()
                return redirect(url_for('sku'))# clears POST data 


    records, relation = navigate_to(nav_button, conn, form, table_list)
    #personalise record list headers
    column_names =[['SKUs',['id', 'Name', 'related to', 'Content', 
                    '', 'Barcode','Image', 'Pref Vendor',
                    'Itbis', 'Empty weight', '', 
                    'enabled']]]
    
    sku_img_name = sel.all(db, table_list[0], id = form.id.data)[0].get('sku_foto')

    if not sku_img_name:
        sku_img = session['sku_notimg']
    else:
        session['sku_img'] = sku_img = url_for('static', 
            filename = 'skupics/' + sku_img_name) 

    return render_template ('sku.html', form = form, records = records,
                            column_names = column_names, 
                            sku_unit_choices = sku_unit_choices,
                            sku_ingr_choices = sku_ingr_choices,
                            sku_pref_choices = sku_pref_choices,
                            sku_img = sku_img
                            )


@app.route('/templates/receive.html', methods=['GET','POST'])
def receive():
    form = Rcv_en()
    table_list = ['logix_en', 'logix_de']
    
    #Queries for Selectfields active choices
    form.lox_vend.choices = sel.ebld_choices(db, 'socio', 'soc_name', 'soc_ebld')
    form.subform.log_alm.choices = sel.ebld_choices(db, 'almacen', 'alm_name', 'alm_ebld')
    form.subform.log_sku.choices = sel.ebld_choices(db, 'sku', 'sku_name', 'sku_ebld')

    #Queries for all Selectfields choices
    lox_vend_choices = sel.all_choices(db, 'socio', 'soc_name') 
    log_alm_choices = sel.all_choices(db, 'almacen', 'alm_name')
    log_sku_choices = sel.all_choices(db, 'sku', 'sku_name')

    #if request.form.get('nav') is None --> its a redirect 
    #--> its either an update, new or deleted record hence not necesarilly 
    #last record should be displayed 
    if request.form.get('nav'):
        nav_button =  request.form.get('nav') #saves form navigation request
    else:
        nav_button = session.get('curr_rcd_' + type(form).__name__)

    session['sub_nav_button'] = request.form.get('subnav') #saves subform navigation request
    session['delete_id'] = request.form.get('delete')

    try:
        nav_button = int(nav_button)
    except:
        pass
    
    try:
        session['sub_nav_button'] = int(session['sub_nav_button'])
    except:
        pass

    try:
        session['delete_id'] = int(session['delete_id'])
    except:
        pass    

    print('formvalidate', form.validate_on_submit())

    if form.validate_on_submit():

        listsql = listsql2 = {
                                table_list[0]:[{
                                    'id':form.id.data,
                                    'lox_date':form.lox_date.data,
                                    'lox_datd':form.lox_datd.data,
                                    'lox_vend':form.lox_vend.data,
                                    'lox_nifn':form.lox_nifn.data,
                                    'lox_doc_no':form.lox_doc_no.data,
                                    'lox_disc':form.lox_disc.data,
                                    'lox_sub':form.lox_sub.data,
                                    'lox_tax':form.lox_tax.data
                                            }],
                                table_list[1]:[{
                                    'id':form.subform.idx.data,
                                    'log_enca':form.subform.log_enca.data,
                                    'log_sku':form.subform.log_sku.data,
                                    'log_qty':form.subform.log_qty.data,
                                    'log_pric':form.subform.log_pric.data,
                                    'log_tax':form.subform.log_tax.data,  
                                    'log_alm':form.subform.log_alm.data,
                                    'log_wtax':form.subform.log_wtax.data 
                                            }]
                                
                            }
        listsql1 ={list(listsql.keys())[0]: list(listsql.values())[0]}

        del listsql2 [list(listsql.keys())[0]]
        if not form.id.data: #gives form.id.data some value on very first entry
            form.id.data = 0

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
                return redirect(url_for('receive'))# clears POST data

            else:
                #adds new record
                session['curr_rcd_' + type(form).__name__] = None 
                    # ^ so it navigates to the last record after adding
                record.add_new(lox_rece = 1)
                return redirect(url_for('receive'))# clears POST data 

        if nav_button == "submit1": #not a nav post
            
            #completes missing receipt item price or tax  info when left blank
            #unique for this form

            sql = "SELECT sku_itbi FROM sku WHERE id = {}".format(form.subform.log_sku.data)
            db.execute(sql)
            dbtax = db.fetchall()[0].get('sku_itbi')
            if not form.subform.log_qty.data:
                listsql2.get(table_list[1])[0]['log_qty'] = 0
            if bool(form.subform.log_pric.data == None) ^ bool(form.subform.log_tax.data == None):
                if not form.subform.log_pric.data:
                    if form.subform.log_wtax.data:
                        listsql2.get(table_list[1])[0]['log_pric'] = form.subform.log_tax.data * (1 + dbtax) / dbtax
                    else:
                        listsql2.get(table_list[1])[0]['log_pric'] = form.subform.log_tax.data / dbtax
                else:
                    if form.subform.log_wtax.data:
                        listsql2.get(table_list[1])[0]['log_tax'] = listsql2.get(table_list[1])[0].get('log_pric') * dbtax / (1 + dbtax)
                    else:
                        listsql2.get(table_list[1])[0]['log_tax'] = listsql2.get(table_list[1])[0].get('log_pric') * dbtax
            else:
                    if form.subform.log_wtax.data:
                        listsql2.get(table_list[1])[0]['log_tax'] = listsql2.get(table_list[1])[0].get('log_tax') or 0
                        listsql2.get(table_list[1])[0]['log_pric'] = (listsql2.get(table_list[1])[0].get('log_pric') or 0 ) - (listsql2.get(table_list[1])[0].get('log_tax') or 0)
                    else:
                        listsql2.get(table_list[1])[0]['log_tax'] = listsql2.get(table_list[1])[0].get('log_tax') or 0
                        listsql2.get(table_list[1])[0]['log_pric'] = listsql2.get(table_list[1])[0].get('log_pric') or 0

            
            #creates instance to chk if record exist
            record = dth.from_dict2sql(conn, listsql2)
            existe = dth.from_dict2sql(conn, {
                                        table_list[1]:[{
                                            'id':form.subform.idx.data
                                                    }]
                                        }
            )   

            if  existe.chk_sgl_fld():   #chk if record exists   
                #update existing record
                record.update()
                update.stockqty(db, list(listsql2.keys())[0], 
                    list(listsql2.values())[0][0].get('id'), 
                    list(listsql2.values())[0][0].get('log_qty'))
                return redirect(url_for('receive'))# clears POST data

            else:
                #adds new record
                record.add_new()
                return redirect(url_for('receive'))# clears POST data
        
        if session['delete_id']:
            dlt.id(conn, table_list[1], session['delete_id'])
            return redirect(url_for('receive'))# clears POST data

            
    records, relation = navigate_to(nav_button, conn, form, table_list)
    session['relation'] = relation

    records.pop(0) #form header records not needed nav populates header

    column_names =[['Receipt items',['', '', 'SKU', 'Qty', 'Total Price',
                     'Total Tax', 'Price has tax incld']]]
    rcd_len = len(records)

    #checks if line items price includes tax for current vendor displayed
    #unique for this form
    session['flexSwitch'] = 1
    if form.lox_vend.data:
        sql = "SELECT soc_wtax FROM socio WHERE id = {}".format(form.lox_vend.data)
        db.execute(sql)
        session['flexSwitch'] = db.fetchall()[0].get('soc_wtax')

    #updates aggregate fields in form
    #unique for this form
    aggrfields = sel.sumfields(db,'logix_de_norm','log_pric','log_tax',log_enca=form.id.data)[0]
    if aggrfields.get('sumoflog_pric'):
        form.lox_sub.data = aggrfields.get('sumoflog_pric')
    else:    
        form.lox_sub.data = 0
        
    if aggrfields.get('sumoflog_tax'):   
        form.lox_tax.data = aggrfields.get('sumoflog_tax')
    else:
        form.lox_tax.data = 0

    if not form.lox_disc.data:
        form.lox_disc.data = 0

    session['Sub-total'] = form.lox_sub.data - form.lox_disc.data
    session['Total'] = session['Sub-total'] + form.lox_tax.data
    

    return render_template ('receive.html', form = form, records = records,
                            column_names = column_names, 
                            lox_vend_choices = lox_vend_choices,
                            log_alm_choices = log_alm_choices,
                            log_sku_choices = log_sku_choices,
                            relation = relation,
                            rcd_len = rcd_len)


if __name__ == '__main__':
    app.run(debug=True)