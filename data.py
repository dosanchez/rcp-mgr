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
    def all(db, tbl):
        sql = "Select * from {}".format(tbl)
        db.execute(sql)
        return(db.fetchall())

    def max_id(db, tbl):
        sql = "Select MAX(id) AS parent_last_row_id from {}".format(tbl)
        db.execute(sql)
        return(db.fetchall())

    #Queries for active (ebld) choices
    def UM_ebld(db):
        
        sql = """SELECT id, uni_symb 
                FROM unitmeas
                WHERE uni_ebld = True"""
        db.execute(sql)
        return sorted([(d['id'], d['uni_symb']) for d in list(db.fetchall())],
                        key = lambda fld: fld[1])
    
    def ingred_ebld(db):
        sql = """SELECT id, ing_name 
            FROM ingredient
            WHERE ing_ebld = True""" 
        db.execute(sql)
        return sorted([(d['id'], d['ing_name']) for d in list(db.fetchall() )], 
                        key = lambda fld: fld[1])

    #Queries for all choices
    def UM_all(db):
        
        sql = """SELECT id, uni_symb 
                FROM unitmeas"""
        db.execute(sql)
        return sorted([(d['id'], d['uni_symb']) for d in list(db.fetchall())],
                        key = lambda fld: fld[1])

    def ingred_all(db):
        sql = """SELECT id, ing_name 
            FROM ingredient""" 
        db.execute(sql)
        return sorted([(d['id'], d['ing_name']) for d in list(db.fetchall() )], 
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

            flash('Record updated!')


    def add_new(self):
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