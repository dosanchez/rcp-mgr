import mysql.connector
from flask import flash, session

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
            
            db.execute(sql[:-4]) 
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
    def UM_ebld(db, blank = False):
        """returns a set with Enable unit of measure"""
        sql = """SELECT id, uni_symb 
                    FROM unitmeas
                    WHERE uni_ebld = True"""
        db.execute(sql)
        
        if blank == True:
            choice = [(None,'---')]
        else:
            choice =[]
        
        return choice + sorted([(d['id'], d['uni_symb']) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])



    def ingred_ebld(db, blank = False):
        sql = """SELECT id, rct_name 
            FROM recet_en
            WHERE rct_ebld = True""" 
        db.execute(sql)

        if blank == True:
            choice = [(None,'---')]
        else:
            choice =[]

        return choice + sorted([(d['id'], d['rct_name']) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])

    def bp_ebld(db, blank = False):
        sql = """SELECT id, soc_name 
            FROM socio
            WHERE soc_ebld = True""" 
        db.execute(sql)

        if blank == True:
            choice = [(None,'---')]
        else:
            choice =[]

        return choice + sorted([(d['id'], d['soc_name']) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])

    #Queries for all choices
    def UM_all(db, blank = False):
        
        sql = """SELECT id, uni_symb 
                FROM unitmeas"""
        db.execute(sql)

        if blank == True:
            choice = [(None,'---')]
        else:
            choice =[]

        return choice + sorted([(d['id'], d['uni_symb']) for d in list(db.fetchall())],
                        key = lambda fld: fld[1])

    def ingred_all(db, blank = False):
        sql = """SELECT id, rct_name 
            FROM recet_en""" 
        db.execute(sql)

        if blank == True:
            choice = [(None,'---')]
        else:
            choice =[]

        return choice + sorted([(d['id'], d['rct_name']) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])
    
    def bp_all(db, blank = False):
        
        sql = """SELECT id, soc_name 
                FROM socio"""
        db.execute(sql)

        if blank == True:
            choice = [(None,'---')]
        else:
            choice =[]

        return choice + sorted([(d['id'], d['soc_name']) for d in list(db.fetchall())],
                        key = lambda fld: fld[1])

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
                    if not fn == 'id':
                        sql += "%s = %s, " %(fn, fv)    
                sql += "WHERE id = %s" %(ea_rcd['id'])
                sql = sql.replace(", WHERE id =", " WHERE id =") #removes trailing ,
                self.conn.cursor(dictionary=True, buffered=True).execute(sql)
                self.conn.commit()
                print('sql', sql)

            flash('Record updated!')


    def add_new(self, **kwargs):
        """adds record in table based on dict with tbl, fld and vals"""
        db = self.conn.cursor(dictionary=True, buffered=True)
        print('rcd',self.rcd)
        print('kwargs', kwargs)
        if not session.get('relation'):
            session['relation'] = [[{}]]
        counter = 0
        for t, r in self.rcd.items():
            value_str = ') VALUES('
            counter += 1
            for ea_rcd in r:
                sql = "INSERT INTO %s (" %(t)
                for fn, fv in ea_rcd.items():
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
            for t, r in rcd.items():
                for ea_rcd in r:
                    for fn, fv in ea_rcd.items():
                        if isinstance(fv, str):
                            ea_rcd[fn]="\'" + fv + "\'"
            
            return cls(conn, rcd)
        else:
            rcd = {}
        
        return cls(db, rcd)