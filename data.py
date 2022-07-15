from genericpath import exists
import mysql.connector
from flask import Flask, flash, render_template, request, session, redirect, url_for


class DataHandler():

    def __init__(self, db, rcd = None):
        
        self.db = db
        if not rcd:
            self.rcd ={}
        else:
            self.rcd = rcd    
        

    def chk_sngl_fld(self): 
        """checks if a single value already exists in a single table field"""



        if len(self.rcd.get('fields')) == 1: 
        
            table = list(self.rcd.values())[0]
            field = list(self.rcd.get('fields'))[0]
            value = self.rcd.get('fields').get(field)
            print(table, field, value)
            sql = "SELECT COUNT(%s) AS existe FROM %s WHERE %s = '%s'" %(field, table, field, value)
            print(sql)
            self.db.execute(sql)
            record = self.db.fetchone()
            if record.get('existe') == 1:
                return True
            else:
                return False

        return False

    # @classmethod
    # def from_base(cls, rcd = None):
        