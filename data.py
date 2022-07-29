import mysql.connector
from flask import flash


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
        counter = 0
        for t, r in self.rcd.items():
            for ea_rcd in r:
                counter += 1
                sql = "UPDATE %s SET " %(t)
                for fn, fv in ea_rcd.items():
                    if not fn == 'id':
                        sql += "%s = %s, " %(fn, fv)    
                sql += "WHERE id = %s" %(ea_rcd['id'])
                sql = sql.replace(", WHERE id =", " WHERE id =") #removes last ,
                self.conn.cursor(dictionary=True, buffered=True).execute(sql)
                self.conn.commit()
        
        if counter > 1:
            flash('Records updated!')
        elif counter == 1:
            flash('Record updated!')
        else:
            pass

    def add_new(self):
        """adds record in table based on dict with tbl, fld and vals"""
        counter = 0
        value_str = ') VALUES('
        for t, r in self.rcd.items():
            for ea_rcd in r:
                counter += 1
                sql = "INSERT INTO %s (" %(t)
                for fn, fv in ea_rcd.items():
                    if not fn == 'id':
                        sql += "%s, " %(fn)
                        value_str += "%s, " %(fv)   
                sql +=value_str + ')'
                sql = sql.replace(", )", ")") #removes extra ,
                self.conn.cursor(dictionary=True, buffered=True).execute(sql)
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