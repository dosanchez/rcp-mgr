import datetime
from flask import flash, session
import os, secrets
from PIL import Image
import json


def save_file(sku_pic, save_path, f_name = None):
    #selects current name or creates one if none with new pic extension
    _, fext = os.path.splitext(sku_pic.filename)
    if not f_name:    
        randon_name = secrets.token_hex(4)
        f_name = randon_name + fext
        new_name = f_name
    else:
        name = f_name.split('.')[0]
        new_name = name + fext
   
   #stores old and new name + path
    pic_path = os.path.join(save_path, f_name)
    new_path = os.path.join(save_path, new_name)
   
    #scales image
    new_size = (240, 320)
    resized_img = Image.open(sku_pic)
    resized_img.thumbnail(new_size)

    #saves new image with old name then changes the name to new one
    resized_img.save(pic_path)
    os.rename(pic_path, new_path)
    
    return new_name


class dlt():
    def id(conn, tbl, id):
        db = conn.cursor(dictionary=True, buffered=True)
        sql = "DELETE FROM {} WHERE id = {}".format(tbl, id)
        db.execute(sql)
        conn.commit()
        flash('record deleted', 'alert alert-warning')


class select():
    """various query select functions """
    
    #various queries
    def UMconv(db, qty, knownbaseUM, targetbaseUM, sku=None, ingr= None, matrix=None):
        """returns the value in a target unit of Measure of a qty with
         a base unit of measure, given a sku, ingredient or a conversion matrix"""
        
        if sku:
            pass
        elif ingr:
            pass
        elif matrix:
            return(qty*matrix.get(targetbaseUM + "/" + knownbaseUM))
        return 0

    


    def recipesforingr(db, ingr):
        """returns a tuple with all recipes containing a specific ingredient"""
        sql ="""WITH RECURSIVE 
                    bom AS (SELECT  prnt.id, chld.rcd_ing AS 'ingr', chld.rct_rece
                            FROM recet_en AS prnt
                            LEFT JOIN chld
                            ON prnt.id = chld.rcd_enca
                            WHERE prnt.rct_rece = 1
                            
                            UNION ALL
                            
                            SELECT  bom.id, chld.rcd_ing AS 'ingr', chld.rct_rece
                            FROM bom
                            LEFT JOIN chld
                            ON ingr = chld.rcd_enca
                            WHERE bom.rct_rece = 1
                            
                            
                        ),
                                
                    chld AS  (SELECT rcd_ing, rcd_enca, subchld.rct_rece  
                            FROM  recet_de
                            LEFT JOIN recet_en AS subchld
                            ON recet_de.rcd_ing = subchld.id)
                                
            SELECT id 
            FROM bom
            WHERE rct_rece = 0 AND ingr = {}""".format(ingr)
        db.execute(sql)
        rcptlist = tuple(rcd.get('id') for rcd in db.fetchall())

        return(rcptlist)

    def bom(conn:'connection to database', recipes:'list with recipes numbers' = None, byrecipe:'True sum up by recipe False sum up all ingrd'=False):
        """special function to sum up all ingredient quantities needed for one, a group
        or all recipes"""
        sql = """DROP TABLE IF EXISTS bom"""
        conn.cursor().execute(sql)
        conn.commit()

        if byrecipe:
            add1 ='prnt.'
            add2 = 'id'
            add3 = ', '
        else:
            add1 = add2 = add3 = ''

        db = conn.cursor(dictionary= True, buffered=True)
        unit_id = select.all(db, 'unitmeas', uni_symb = 'unit')[0].get('id')
        sql ="""
            WITH RECURSIVE 
                temp_bom AS
                    (	SELECT  chld.rcd_ing AS 'ingr', bom_qty,
                                chld.bs_unit, chld.rct_rece{}{}{}
                        FROM recet_en AS prnt
                        LEFT JOIN chld
                        ON prnt.id = chld.rcd_enca
                        WHERE prnt.rct_rece = 1""".format(add3, add1, add2)
                        
                        
        if recipes:
            sql += ' AND prnt.id IN ('
            for recipe in recipes:
                sql += '{}, '.format(recipe)
            sql = sql[:-2] + ')'

        sql += """ UNION ALL
                        
                        SELECT  chld.rcd_ing AS 'ingr', chld.bom_qty,
                                chld.bs_unit, chld.rct_rece{0}{1}
                        FROM temp_bom
                        LEFT JOIN chld
                        ON ingr = chld.rcd_enca
                        WHERE temp_bom.rct_rece = 1
                        
                        
                    ),

                subprnt AS 	(SELECT rcd_ing, rcd_qty * uni_conv AS rcd_qty, 
                                    uni_un_t AS bs_unit, rcd_yiel, rcd_enca
                            FROM recet_de
                            LEFT JOIN unitmeas
                            ON recet_de.rcd_unit = unitmeas.id),
                            
                chld AS 	(SELECT rcd_ing , bs_unit, rcd_qty/rcd_yiel AS bom_qty, rcd_enca, subchld.rct_rece  
                            FROM  subprnt
                            LEFT JOIN recet_en AS subchld
                            ON subprnt.rcd_ing = subchld.id)
                            
            SELECT {1}{0}ingr, SUM(bom_qty), bs_unit 
            FROM temp_bom
            WHERE rct_rece = 0
            GROUP BY ingr, bs_unit{0}{1}
                    """.format(add3, add2)
                  
        db.execute(sql)

        return(db.fetchall())

      
        
    def sglfld(db, table, field, orderby = 'id', **kwargs):
        """returns a list of dictionaries (records) of a single table given a 
        criteria, order ascending by a certain field"""

        if not kwargs:
            sql = "Select {} FROM {}".format(field, table)
            sql += " ORDER BY {} ASC".format(orderby)
            db.execute(sql)

        else:
            sql = "SELECT {} FROM {} WHERE ".format(field, table)
            for fld, val in kwargs.items():
                if isinstance(val, str):
                    sql += "{} = '{}' ".format(fld, val)
                else:
                    sql += "{} = {} ".format(fld, val)
                sql += "AND "
                sql = sql[:-4] + " ORDER BY id ASC" #drop trailing 'AND '
            db.execute(sql)

        return(db.fetchall())




    def all(db, table, orderby = 'id', **kwargs):
        """returns all records from a given table filtered when given
            ordered asc by given field"""

        if not kwargs:
            sql = "Select * FROM {}".format(table)
            sql += " ORDER BY {} ASC".format(orderby)
            db.execute(sql)

        else:
            sql = "SELECT * FROM {} WHERE ".format(table)
            for field, value in kwargs.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(field, value)
                else:
                    sql += "{} = {} ".format(field, value)
                sql += "AND "
            sql = sql[:-4] + " ORDER BY id ASC" #drop trailing 'AND '  

            db.execute(sql) 

        return(db.fetchall())


    def max_id(db, table, **kwargs):
        """returns max id field value from a given table filtered when given"""
        if not kwargs:
            sql = "Select MAX(id) AS parent_last_row_id from {}".format(table)
            db.execute(sql)
        else:
            sql = "SELECT MAX(id) AS parent_last_row_id FROM {} WHERE ".format(table)
            for field, value in kwargs.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(field, value)
                else:
                    sql += "{} = {} ".format(field, value)
                sql += "AND " 
            db.execute(sql[:-4])
        return(db.fetchall())

    def foreign_tbl(conn, ref_tbl, chld_tbl):
        """returns parent child fields of two given tables"""
        db = conn.cursor(dictionary=True, buffered=True)
        sql ="""SELECT TABLE_NAME AS child_tbl, 
                            COLUMN_NAME AS child_tbl_fld, 
                            REFERENCED_TABLE_NAME AS parent_tbl, 
                            REFERENCED_COLUMN_NAME AS parent_tbl_fld 
                            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = '{}'
                            AND REFERENCED_TABLE_NAME = '{}'
                            AND TABLE_NAME = '{}'
                            AND REFERENCED_COLUMN_NAME = 'id'""".format(conn.database, 
                                ref_tbl, chld_tbl)
        db.execute(sql)
        return db.fetchall()

    def chld_vals(db, ref_tbl, chld_tbl, child_tbl_fld, ref_tbl_id_val):
        """returns a set with all child records for a given parent record id value"""
        sql = """SELECT b.* FROM {} AS h INNER JOIN {} AS b
                ON h.id = b.{}
                WHERE h.id = {}""".format(ref_tbl, chld_tbl, child_tbl_fld, ref_tbl_id_val)
        db.execute(sql)
        return db.fetchall()     

    #Queries for active (ebld) choices
    def ebld_choices(db, table, field, truefield, blank = False, **kwargs):
        """returns a set of (id, <<field>>) tuples for 
            selectfield choices Where a <<truefield>> is True 
            and any field equal to a given value"""

        sql = """SELECT id, {} 
                    FROM {}
                    WHERE {} = True AND""". format(field, table, truefield)
        for fld, value in kwargs.items():
            if isinstance(value, str):
                sql += "{} = '{}' ".format(fld, value)
            else:
                sql += "{} = {} ".format(fld, value)
            sql += "AND "
        
        db.execute(sql[:-4]) #drops trailing AND
        
        if blank:
            choice = [(0,'---')] 
        else:
            choice =[]

        return choice + sorted([(int(d['id']), d[field]) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])



    #Queries for all choices
    def all_choices(db, table, field, blank = False, **kwargs):
        """returns a set of all (id, <<field>>) tuples for 
            selectfield choices"""

        sql = """SELECT id, {} 
                    FROM {}    """. format(field, table)
        if not kwargs == {}:
            sql += "WHERE "
            for fld, value in kwargs.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(fld, value)
                else:
                    sql += "{} = {} ".format(fld, value)
                sql += "AND "

        db.execute(sql[:-4]) #drops trailing AND
        
        if blank:
            choice = [(0,'---')]   
        else:
            choice =[]

        return choice + sorted([(int(d['id']), d[field]) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])
    #adds up given fields for specific table and specific where field value
    def sumfields(db, table, *args, **kwargs):
        """returns the sum of given fields given specific fields values"""
        sql = "SELECT "
        for value in args:
                sql += "SUM({}) AS {}, ".format(value, 'sumof'+ value )
                
        sql += "FROM {} ".format(table)
        sql = sql.replace(", F", " F") #removes trailing ,
        sql += "WHERE "
        for field, value in kwargs.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(field, value)
                else:
                    sql += "{} = {} ".format(field, value)
                sql += "AND " 
        print('sql in sumfields', sql)
        db.execute(sql[:-4]) #drops trailing AND
        return(db.fetchall())
    
    
    def secondfromtop(db, table, secondfor= 'id', max = None, **kwargs):
        """special function to get 2nd highest record for a field (secondfor)
        with a given filter, a top field(secondfor) can be given"""

        sql = "Select {} FROM {} WHERE ".format(secondfor, table)

        if not kwargs:
            if not max:
                sql+= sql[:-7] #drop trailing 'WHERE '
            else:
                if isinstance(max, str):
                    max =int(max.strip(' \"\' '))
                sql +="{} <= {}".format(secondfor, max)
        else:
            for field, value in kwargs.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(field, value)
                else:
                    sql += "{} = {} ".format(field, value)
                sql += "AND "
                
                if not max:
                    sql = sql[:-4] #drop trailing 'AND '
                else:
                    if isinstance(max, str):
                        max =int(max.strip(' \"\' '))
                    sql +="{} <= {}".format(secondfor, max)

        sql += " ORDER BY {} DESC LIMIT 1,1".format(secondfor)
        db.execute(sql) 
        result = db.fetchall()
       
        if not result or not result[0]:
            return 0
        else:
            return result[0].get(secondfor)


class update():
    def field(conn, table, field, value, **kwargs):
        """updates a single field from a table with a value 
        given a criteria"""
        
        sql = "UPDATE {} SET ".format(table)
        if isinstance(value, str):
            sql += "{} = '{}' ".format(field, value)
        else:
            sql += "{} = {} ".format(field, value)
           
        if not kwargs:
            pass
        else:
            sql += "WHERE " 
            for filter, arg in kwargs.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(filter, arg)
                else:
                    sql += "{} = {} ".format(filter, arg)
                sql += "AND "
            sql = sql[:-4] #drop trailing 'AND '
        conn.cursor().execute(sql)
        conn.commit()


    def cumfield(conn, table, id, basefield, cumfield, **kwargs):
        """updates cumulative field from a base field in a table
            for a given criteria from a given id on. Returns
            id and Cumulated value"""
        if isinstance(id, str):
            id =int(id.strip(' \"\' '))

        runningbal = 0
        rcds =select.all(conn.cursor(dictionary=True, buffered=True), table)
        
        for dict in rcds:
            if kwargs.items() <= dict.items():
                if dict.get('id') == id:
                    runningbal = dict.get(cumfield)
                if dict.get('id') > id:
                    runningbal += dict.get(basefield)
                    sql = """UPDATE {} 
                            SET {} = {} 
                            WHERE id = {} """.format(table, cumfield,
                                                    runningbal, 
                                                    dict.get('id'))
                    
                    conn.cursor(dictionary=True, buffered=True).execute(sql)
                    conn.commit()
    
    def stockweightedcost(conn, table, id, basefield, cumfield, cumweightfield, **kwargs):
        """Special function that calculates Stock weighted cost for each sku"""

        if isinstance(id, str):
            id =int(id.strip(' \"\' '))

        runningbal = 0
        runningweight = 0
        rcds =select.all(conn.cursor(dictionary=True, buffered=True), table + '_norm')
        
        for dict in rcds:
            if kwargs.items() <= dict.items():
                if dict.get('id') == id:
                    runningbal = dict.get(cumfield)
                    runningweight = dict.get(cumweightfield)

                if dict.get('id') > id:

                    runningbal = (runningweight*runningbal + dict.get(basefield))/ dict.get(cumweightfield)
                    runningweight = dict.get(cumweightfield)
                    sql = """UPDATE {} 
                            SET {} = {} 
                            WHERE id = {} """.format(table, cumfield,
                                                    runningbal, 
                                                    dict.get('id'))
                    
                    conn.cursor(dictionary=True, buffered=True).execute(sql)
                    conn.commit()

    def costupdate(conn, sku= None, ingr = None, recipe = None):
        """either updates cost info of ingredients and recipes or updates
            field with missing density values needed to make cost calculations"""
        
        #first lets check if addl density info is needed 
        if not sku and not ingr and not recipe:
            return
        db = conn.cursor(dictionary= True, buffered=True)

        if recipe:
            #Recipe details changed lets update cost of recipes in table recet_en
            #lets update cost if recipecost includes our recipe
            #if not, recipe cost updated to 0 and message flashed 
            sql ="""SELECT *
                    FROM recipecost
                    WHERE recipeid = {}""".format(recipe)
            db.execute(sql)
            if db.rowcount > 0:
                sql = """UPDATE recet_en
                        INNER JOIN recipecost
                        ON id = recipeid
                        SET rct_cosc = cost
                        WHERE id = {}""".format(recipe)
            else:
                sql = """UPDATE recet_en
                        SET rct_cosc = 0
                        WHERE id = {}""".format(recipe)
                flash ("""Unable to cost recipe either because at least one 
                            recipe ingredient have not been received in stock 
                            or there's missing recipe ingredient density info.
                            MRP calculations may no be possible.""",
                             'alert alert-warning')       
            db.execute(sql)
            conn.commit()
            return

        if sku:
            sql = """WITH unit AS (
                            WITH ingred AS (
                                    SELECT sku_ingr AS input
                                    FROM sku
                                    WHERE sku.id = {}
                                            ),

                                subunit AS (
                                    SELECT sku.id, sku_ingr, uni_un_t
                                    FROM sku
                                    LEFT JOIN unitmeas
                                    ON sku_unit = unitmeas.id
                                            )

                            SELECT id as sku, sku_ingr, uni_un_t
                            FROM ingred
                            LEFT JOIN subunit
                            ON input = sku_ingr
                                    )
                    SELECT uni_un_t AS skuunit, rct_dens AS dens, rct_denu AS denu, 
                        rct_dens_1 AS dens1, rct_denu_1 AS denu1, sku, 
                        id
                    FROM recet_en
                    INNER JOIN unit
                    ON id = sku_ingr
                    WHERE rct_rece = 0""".format(sku)

        if ingr:
            sql = """WITH unit AS (

                        SELECT sku.id as sku, sku_ingr, uni_un_t
                        FROM sku
                        LEFT JOIN unitmeas
                        ON sku_unit = unitmeas.id)

                    SELECT DISTINCT uni_un_t AS skuunit, rct_dens AS dens, 
                                rct_denu AS denu, rct_dens_1 AS dens1, 
                                rct_denu_1 AS denu1, sku, recet_en.id
                    FROM recet_en
                    LEFT JOIN unit
                    ON recet_en.id = sku_ingr
                    WHERE recet_en.id = {} AND rct_rece = 0""".format(ingr)

        #stops execution if no output from previous sql statements
        #this should only happen when a recipe related sku is added or changed
        db.execute(sql)
        if db.rowcount < 1:
            flash("""Info: SKU is a recipe substitute""", 'alert alert-info')
            return

        results = db.fetchall()
        skus =[]
        set1 = set()
        set2 = set()
        for rcd in results:
            if not rcd.get('sku') == None:
                skus.append(rcd.get('sku'))
                set1.add(rcd.get('skuunit'))
            if rcd.get('denu'):
                set2.update(rcd.get('denu').rsplit("/"))
            if rcd.get('denu1'):
                set2.update(rcd.get('denu1').rsplit("/"))
            ingrname = rcd.get('rct_name')
            ingr = rcd.get('id')

        missing = set1.difference(set2)
        if missing == set():
            missunit = None
        else:
            missunit = list(missing)[0]
            
            
        #updates necessary fields
        if not missunit:
            #in this case no density is missing let's make a conversion matrix
            sql = """INSERT INTO mtrx_conv
                    VALUES """
            mtrx={}
            densinfo = results[0]
            if not densinfo.get('dens') == None :
                density = densinfo.get('dens')
                baseUM = densinfo.get('denu').split("/")[1]
                targetUM = densinfo.get('denu').split("/")[0]
                mtxid = str(ingr) + targetUM + baseUM
                mtrx[densinfo.get('denu')] = float(density)
                sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                            targetUM, baseUM, density)
                mtxid = str(ingr) + baseUM + targetUM
                mtrx[baseUM +'/'+ targetUM] = float(1 / density)
                sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                            baseUM,targetUM,1/density)

                
            if not densinfo.get('dens1') == None :
                density = densinfo.get('dens1')
                baseUM = densinfo.get('denu1').split("/")[1]
                targetUM = densinfo.get('denu1').split("/")[0]
                mtxid = str(ingr) + targetUM + baseUM
                mtrx[densinfo.get('denu1')] = float(density)
                sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                            targetUM, baseUM, density)
                mtxid = str(ingr) + baseUM + targetUM
                sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                            baseUM, targetUM, 1/density)
                mtrx[baseUM+'/'+ targetUM] = float(1 / density)

            if len(mtrx) > 2:
                if not 'g/ml' in mtrx.keys():
                    density = mtrx.get('g/unit') * mtrx.get('unit/ml')
                    baseUM = 'ml'
                    targetUM = 'g'
                    mtxid = str(ingr) + targetUM + baseUM
                    mtrx['g/ml'] = float(density)
                    sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                            targetUM, baseUM, density)
                    mtrx['ml/g'] = float(1 / mtrx.get('g/ml'))
                    mtxid = str(ingr) + baseUM + targetUM
                    sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                                baseUM, targetUM, 1/density)
                elif not 'g/unit' in mtrx.keys():
                    density = mtrx.get('g/ml') * mtrx.get('ml/unit')
                    baseUM = 'unit'
                    targetUM = 'g'
                    mtxid = str(ingr) + targetUM + baseUM
                    mtrx['g/unit'] = float(density)
                    sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                            targetUM, baseUM, density)
                    mtrx['unit/g'] = float(1 / mtrx.get('g/unit'))
                    mtxid = str(ingr) + baseUM + targetUM
                    sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                                baseUM, targetUM, 1/density)
                else:
                    density = mtrx.get('ml/g') * mtrx.get('g/unit')
                    baseUM = 'unit'
                    targetUM = 'ml'
                    mtxid = str(ingr) + targetUM + baseUM
                    mtrx['ml/unit'] = float(density)
                    sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                            targetUM, baseUM, density)
                    mtxid = str(ingr) + baseUM + targetUM
                    sql += """('{}',{},'{}','{}',{}),""".format(mtxid, ingr,
                                                baseUM, targetUM, 1/density)
                    mtrx['unit/ml'] = float(1 / mtrx.get('ml/unit'))

            sql += """('{0}gg',{0},'g','g',1), ('{0}mlml',{0},'ml','ml',1),
                        ('{0}unitunit',{0},'unit','unit',1)
                        ON DUPLICATE KEY UPDATE mtx_conv = values(mtx_conv)
                        """.format(ingr)
            db.execute(sql)
            conn.commit()

            #ingrcost view now includes cost info for ingredients
            #also recipe cost view now includes cost info for recipes
            #now lets calculate and update recipe costs
            #for that lets find out recipes involved
            rcps = select.recipesforingr(db, ingr)
            
            #lastly lets update cost of recipes in table recet_en
            #lets update cost if recipecost includes our recipe
            #and if any recipe contains the ingredient in question
            #if not recipe cost updated to 0 and message flashed 
            if not rcps == ():

                sql ="""SELECT *
                        FROM recipecost
                        WHERE recipeid IN {}""".format(rcps)
                db.execute(sql)
                if db.rowcount > 0:
                    sql = """UPDATE recet_en
                            INNER JOIN recipecost
                            ON id = recipeid
                            SET rct_cosc = cost
                            WHERE id IN {}""".format(rcps)
                else:
                    sql = """UPDATE recet_en
                            SET rct_cosc = 0
                            WHERE id IN {}""".format(rcps)
                    flash ("""Unable to cost recipe(s) either because some or no recipe(s) 
                                ingredient(s) have been received into stock """,
                                'alert alert-warning')       
                db.execute(sql)
                conn.commit() 
            else:
                flash ("""Info: SKU is either a recipe substitute or it's
                            related ingredient is not used by any recipe""",
                                'alert alert-info') 
        else:
            #since we need more info for costing, lets write down the necessary
            #density for a complete conversion matrix
            missdensUM = [i for i in ['g/ml', 'g/unit', 'ml/unit'] if missunit in i]
            sql ="""UPDATE recet_en 
                    SET rct_misd_dens = '{}'
                    WHERE id = {}""".format(json.dumps(missdensUM) ,ingr)
            db.execute(sql)
            conn.commit()

            flash ("""Due to the recent update, additional density info is 
                        needed in {} under the ingredients menu. if not updated, 
                        recipe cost and MRP calculations will no be possible.
                         """.format(ingrname), 'alert alert-warning')

        return


class DataHandler():

    def __init__(self, conn, rcd = None):
        
        self.conn = conn
        if not rcd:
            self.rcd ={}
        else:
            self.rcd = rcd
        
    def chk_sgl_fld(self): 
        """checks if a single value already exists in a single table field"""

        table = list(self.rcd.keys())[0]    #checks if only sgl tbl, fld,val
        if len(self.rcd.get(table)[0]) == 1: #checks if only sgl tbl, fld,val
        
            field = list(self.rcd.get(table)[0].keys())[0]
            value = self.rcd.get(table)[0].get(field)
            
            sql = """SELECT EXISTS (SELECT * FROM %s WHERE %s = %s) 
                        AS existe""" %(table, field, value)
            print('sql in chcsgl', sql)
            db = self.conn.cursor(dictionary=True, buffered=True)
            db.execute(sql)
            record = db.fetchall()

            if record[0].get('existe') >= 1:
                return True
            else:
                return False
        return False


    def update(self):
        """update record in table based on dict with tbl, fld and vals
            NEEDS an id field for update condition"""
        
        for t, r in self.rcd.items():
            for ea_rcd in r:
                sql = "UPDATE %s SET " %(t)
                for fn, fv in ea_rcd.items():
                    if not fv and fv != 0:
                        fv = 'NULL'
                        
                    if not fn == 'id':
                        sql += "%s = %s, " %(fn, fv)    
                sql += "WHERE id = {}" .format(ea_rcd.get('id'))
                sql = sql.replace(", WHERE id =", " WHERE id =") #removes trailing ,
                self.conn.cursor(dictionary=True, buffered=True).execute(sql)
                self.conn.commit()

            flash('Record updated!', 'alert alert-success')


    def add_new(self, **kwargs):
        """adds record in table based on dict with tbl, fld and vals"""
        db = self.conn.cursor(dictionary=True, buffered=True)
        if not session.get('relation'):
            session['relation'] = [[{}]]
        counter = 0
        for t, r in self.rcd.items():
            value_str = ') VALUES('
            counter += 1
            for ea_rcd in r:
                sql = "INSERT INTO %s (" %(t)
                for fn, fv in ea_rcd.items():
                    if not fv and fv != 0:
                        fv = 'NULL'
                    if fn == session.get('relation')[0][0].get('child_tbl_fld'):
                        sql += "%s, " %(fn)
                        if not session['id'] == 0:
                            value_str += "%s, " %(session['id'])
                        else:
                            value_str += "%s, " %(select.max_id(db, 
                                session.get('relation')[0][0].get('parent_tbl')))

                    elif not fn == 'id':
                        sql += "%s, " %(fn)
                        value_str += "%s, " %(fv)
                
                for k,v in kwargs.items():
                    sql += "%s, " %(k)
                    value_str += "%s, " %(v)

                sql +=value_str + ')'
                sql = sql.replace(", )", ")") #removes trailing ,
                db.execute(sql)
                self.idadded = db.lastrowid
                self.conn.commit()
                
        
        if counter > 1:
            flash('Records added!', 'alert alert-success')
        elif counter == 1:
            flash('Record added!', 'alert alert-success')
        else:
            pass


    @classmethod
    def from_dict2sql(cls, conn, rcd = None):
        """put str dict data between quotes for SQL statement"""
        if rcd:
            for _, r in rcd.items():
                for ea_rcd in r:
                    for fn, fv in ea_rcd.items():
                        if isinstance(fv, datetime.date) and fv:
                            fv = fv.strftime("%Y-%m-%d")
                        if isinstance(fv, str) and fv:
                            ea_rcd[fn] = "\'" + fv + "\'"
            
            return cls(conn, rcd)
        else:
            rcd = {}
        
        return cls(conn, rcd)