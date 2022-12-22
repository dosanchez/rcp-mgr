# rcp-mgr

THIS README IS NOT YET FINISHED
This is my first web app (under construction).  It helps manage recipe costs and related ingredients and finished plates operations.
its based on mysql, flask, WTForms, bootstrap 5
each form can navigate through records while either listing them all at the bottom or listing related records at the bottom.

the challenge is not the app itself but, besides practicing coding skills, design the code in a "modular" way such that adding functionality (new forms) and maintaining it becomes easy with the less code possible

data format to pass to datahandler class (db, {table1name:[{record1field1name:record1field1value},{record1field2name:record1field2value},{record2field1name:record2field1value},{record2field2name:record2field2value}...],table2name:[{record1field1name:record1field1value},{record1field2name:record1field2value},...]})
table1name should always the parent table-form, all other table names should be child or non related tables

Mysql or MariaDB with CTE needed

All database tables must contain an autoincrement field named id as primary  key
id field value must be > 0

foreign key of parent-child tables must be referentially enforced

All wtf Classes are within forms.py
Subforms are defined as inherited classes in WTF.  The subform class id field must be named "idx" not id
Subforms can not contain another subform, however a parent form can contain many subforms

nav.py takes care of form navigation and returns set of registered records

an exception is the ingredient and recipe forms which share same sql table

'-' can not be used in fields or form (class) names

elifs in htmls are used for particular formatting of certain fields else clause is used for cases in general

unitmeas table must have the following records 1g = 1g, 1 ml = 1ml and 1 unit = 1 ml

database used should 

