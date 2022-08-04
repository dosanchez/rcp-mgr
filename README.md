# rcp-mgr
This is my first web app (under construction).  It helps manage recipe costs and related ingredients and finished plates operations.
its based on mysql, flask, WTForms, bootstrap 5
each form can navigate through records while either listing them all at the bottom or listing related records at the bottom.

data format to pass to datahandler class (db, {table1name:[{record1field1name:record1field1value},{record1field2name:record1field2value},{record2field1name:record2field1value},{record2field2name:record2field2value}...],table2name:[{record1field1name:record1field1value},{record1field2name:record1field2value},...]})
table1name should always the parent table, alll other table names should be child or free tables

All database tables must contain an autoincrement field named id
foreign key field with autoincrement parent must be named id_enca.  One permitted per table

All wtf Classes are in forms.py
Subforms are defined as inherited classes in WTF.  The subform class id field must be named "idx" not id

nav.py takes care of form navigation and returns set of registered records