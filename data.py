from genericpath import exists
from sqlite3 import paramstyle
import sqlite3
import mysql.connector
from flask import Flask, flash, render_template, request, session, redirect, url_for


class DataHandler():

    def __init__(self, db, rcd = None):
        
        self.db = db
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

            self.db.execute(sql)
            record = self.db.fetchall()
            
            if record[0].get('existe') == 1:
                return True
            else:
                return False
        return False

    def update(self):
        """update record in table based on dict with tbl, fld and vals"""
        """NEEDS an id field for update condition"""
        for t, r in self.rcd.items():
            for ea_rcd in r:
                sql = "UPDATE %s SET " %(t)
                for fn, fv in ea_rcd.items():
                    if not fn == 'id':
                        sql += "%s = %s, " %(fn, fv)    
                sql += "WHERE id = %s" %(ea_rcd['id'])
                sql = sql.replace(", WHERE id =", " WHERE id =") #removes last ,
                self.db.cursor(dictionary=True, buffered=True).execute(sql)
                self.db.commit()
        
        flash('Sucessfully updated!')



    @classmethod
    def from_dict2sql(cls, db, rcd = None):
        """put str dict data between quotes for SQL statement"""
        if rcd:
            for t, r in rcd.items():
                for ea_rcd in r:
                    for fn, fv in ea_rcd.items():
                        if isinstance(fv, str):
                            ea_rcd[fn]="\'" + fv + "\'"
            
            return cls(db, rcd)
        else:
            rcd = {}
        
        return cls(db, rcd)