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
        flash('record deleted')


class select():
    """various query select functions """
    
    #various queries
    def UMconv(db, qty, baseUM, targetUM, sku=None, ingr= None, matrix=None):
        """returns the value in a target unit of Measure of a qty with
         a base unit of measure, given a sku, ingredient or a conversion matrix"""
        
        if sku:
            pass
        elif ingr:
            pass
        elif matrix:
            print(targetUM, baseUM)
            return(qty*matrix.get(targetUM + "/" + baseUM))
        return 0

    def chkmissingdens(conn, sku= None, ingr = None):
        """returns if a density value is missing for a ingredient and which one."""
        
        #checks if addl density info is needed 
        if not sku and not ingr:
            return
        print(sku, ingr)
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
                    SELECT uni_un_t AS unit, rct_dens AS dens, rct_denu AS denu, 
                        rct_dens_1 AS dens1, rct_denu_1 AS denu1, sku, rct_name, 
                        id
                    FROM recet_en
                    INNER JOIN unit
                    ON id = sku_ingr""".format(sku)

        if ingr:
            sql = """WITH unit AS (

                        SELECT sku.id as sku, sku_ingr, uni_un_t
                        FROM sku
                        LEFT JOIN unitmeas
                        ON sku_unit = unitmeas.id)

                    SELECT DISTINCT uni_un_t AS unit, rct_dens AS dens, 
                                rct_denu AS denu, rct_dens_1 AS dens1, 
                                rct_denu_1 AS denu1, sku, rct_name, recet_en.id
                    FROM recet_en
                    LEFT JOIN unit
                    ON recet_en.id = sku_ingr
                    WHERE recet_en.id = {}""".format(ingr)

        db = conn.cursor(dictionary= True, buffered=True)
        db.execute(sql)
        results = db.fetchall()
        skus =[]
        set1 = set()
        set2 = set()
        print('results--->', results)
        for rcd in results:
            if not rcd.get('sku') == None
                skus.append(rcd.get('sku'))
            set1.add(rcd.get('unit'))
            if rcd.get('denu'):
                set2.update(rcd.get('denu').rsplit("/"))
            if rcd.get('denu1'):
                set2.update(rcd.get('denu1').rsplit("/"))
            ingrname = rcd.get('rct_name')
            ingr = rcd.get('id')

        missing = set1.difference(set2)
        print('missing-->', missing)
        if not missing:
            missunit = None
        else:
            missunit = list(missing)[0]
            
            
        #updates necessary fields
        if not missunit:
            #since no density missing let's make a conversion matrix
            mtrx={}
            densinfo = results[0]
            if not densinfo.get('dens') == None :
                mtrx[densinfo.get('denu')] = float(densinfo.get('dens'))
                mtrx[densinfo.get('denu').split("/")[1]+'/'+ densinfo.get('denu').split("/")[0]] = float(1 / densinfo.get('dens'))

            if not densinfo.get('dens1') == None :
                mtrx[densinfo.get('denu1')] = float(densinfo.get('dens1'))
                mtrx[densinfo.get('denu1').split("/")[1]+'/'+ densinfo.get('denu1').split("/")[0]] = float(1 / densinfo.get('dens1'))
            if len(mtrx) > 2:
                if not 'g/ml' in mtrx.keys():
                    mtrx['g/ml'] = float(mtrx.get('g/unit') * mtrx.get('unit/ml'))
                    mtrx['ml/g'] = float(1 / mtrx.get('g/ml'))
                
                elif not 'g/unit' in mtrx.keys():
                    mtrx['g/unit'] = float(mtrx.get('g/ml') * mtrx.get('ml/unit'))
                    mtrx['unit/g'] = float(1 / mtrx.get('g/unit'))
                else:
                    mtrx['ml/unit'] = float(mtrx.get('ml/g') * mtrx.get('g/unit'))
                    mtrx['unit/ml'] = float(1 / mtrx.get('ml/unit'))

            sql = """UPDATE recet_en
                    SET rct_conv_mtrx = '{}',
                    rct_misd_dens = NULL
                    WHERE id = {}""".format(json.dumps(mtrx), ingr)
            db.execute(sql)
            conn.commit()

        else:
            #we need more info, lets write down what density 
            # we need to mke the conversion matrix
            missdensUM = [i for i in ['g/ml', 'g/unit', 'ml/unit'] if missunit in i]
            sql ="""UPDATE recet_en 
                    SET rct_misd_dens = '{}'
                    WHERE id = {}""".format(json.dumps(missdensUM) ,ingr)
            print('missdensUM-->', missdensUM)
            db.execute(sql)
            conn.commit()

        flash ("""Due to the recent update, additional density info is needed in {} under the ingredients menu. 
if not updated, recipe cost and MRP calculations will no be possible. """.format(ingrname), 'warning')

        #lets start with ingredient cost calculation
        #target Unit of Measure for ingredient cost
        costUM = list(mtrx.keys())[0].split("/")[0]
        #cost of ingredient calc and update in recet_en
        


        return


    def recipesforingr(db, ingr):
        """returns a list with all recipes containing a specific ingredient"""
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
        rcptlist = [rcd.get('id') for rcd in db.fetchall()]

        return(rcptlist)

    def bom(conn, recipes= None):
        """special function to sum up all ingredient quantities needed for one, a group
        or all recipes"""
        sql = """DROP TABLE IF EXISTS bom"""
        conn.cursor().execute(sql)
        conn.commit()

        db = conn.cursor(dictionary= True, buffered=True)
        unit_id = select.all(db, 'unitmeas', uni_symb = 'unit')[0].get('id')
        sql ="""
            CREATE TEMPORARY TABLE bom
            WITH RECURSIVE 
                temp_bom AS
                    (	SELECT  chld.rcd_ing AS 'ingr', chld.rcd_qty / chld.rcd_yiel AS bom_qty,
                                chld.rcd_unit, prnt.id, chld.rct_rece, prnt.rct_rece AS recetas
                        FROM recet_en AS prnt
                        LEFT JOIN chld
                        ON prnt.id = chld.rcd_enca
                        WHERE prnt.rct_rece = 1"""
                        
                        
        if recipes:
            sql += ' AND prnt.id IN ('
            for recipe in recipes:
                sql += '{}, '.format(recipe)
            sql = sql[:-2] + ')'

        sql += """ UNION ALL
                        
                        SELECT  chld.rcd_ing AS 'ingr', chld.rcd_qty / chld.rcd_yiel AS bom_qty,
                                chld.rcd_unit, temp_bom.id, chld.rct_rece, temp_bom.recetas
                        FROM temp_bom
                        LEFT JOIN chld
                        ON ingr = chld.rcd_enca
                        WHERE temp_bom.rct_rece = 1
                        
                        
                    ),

                subprnt AS 	(SELECT rcd_ing, rcd_qty * uni_conv AS rcd_qty, 
                                CASE
                                    WHEN rcd_unit = {} THEN 'unit'
                                    ELSE uni_un_t
                                END AS rcd_unit, 
                                rcd_yiel, rcd_enca
                            FROM recet_de
                            LEFT JOIN unitmeas
                            ON recet_de.rcd_unit = unitmeas.id),
                            
                chld AS 	(SELECT rcd_ing, rcd_qty, rcd_unit, rcd_yiel, rcd_enca, subchld.rct_rece  
                            FROM  subprnt
                            LEFT JOIN recet_en AS subchld
                            ON subprnt.rcd_ing = subchld.id)
                            
            SELECT * 
            FROM temp_bom
            WHERE rct_rece = 0
                    """.format(unit_id)
                    
        print(sql)
      
        
    def sglfld(db, table, field, orderby =id, **kwargs):
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
    def ebld_choices(db, table, field, truefield, blank = False):
        """returns a set of (id, <<field>>) tuples for 
            selectfield choices Where a <<truefield>> is True"""

        sql = """SELECT id, {} 
                    FROM {}
                    WHERE {} = True""". format(field, table, truefield)
        db.execute(sql)
        
        if blank:
            choice = [(0,'---')] 
        else:
            choice =[]

        return choice + sorted([(int(d['id']), d[field]) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])



    #Queries for all choices
    def all_choices(db, table, field, blank = False):
        """returns a set of all (id, <<field>>) tuples for 
            selectfield choices"""

        sql = """SELECT id, {} 
                    FROM {}""". format(field, table)
        db.execute(sql)
        
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
        print(sql)
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
                    
                    print(sql)
                    conn.cursor(dictionary=True, buffered=True).execute(sql)
                    conn.commit()

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

            flash('Record updated!')


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
            flash('Records added!')
        elif counter == 1:
            flash('Record added!')
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