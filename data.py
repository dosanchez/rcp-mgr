import datetime
from flask import flash, session
import os, secrets
from PIL import Image


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
    
        
    def all(db, tbl, **kwargs):
        """returns all records from a given table filtered when given"""
        if not kwargs:
            sql = "Select * from {}".format(tbl)
            db.execute(sql)

        else:
            sql = "Select * from {} WHERE ".format(tbl)
            for field, value in kwargs.items():
                if isinstance(value, str):
                    sql += "{} = '{}' ".format(field, value)
                else:
                    sql += "{} = {} ".format(field, value)
                sql += "AND "
            
            db.execute(sql[:-4]) #drop trailing 'AND '
            
        return(db.fetchall())


    def max_id(db, tbl, **kwargs):
        """returns max id field value from a given table filtered when given"""
        if not kwargs:
            sql = "Select MAX(id) AS parent_last_row_id from {}".format(tbl)
            db.execute(sql)
        else:
            sql = "SELECT MAX(id) AS parent_last_row_id FROM {} WHERE ".format(tbl)
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

class update():

    def stockqty(db, table, id, qty):
        print(table)
        print(id)
        print(qty)
        pass

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