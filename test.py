rcd = {'unitmeas':[
                    {
                    'uni_symb':'tonne11',
                    'field1':12,
                    'field2':'primer tres',
                    'id':1
                },
                    {
                    'uni_symb':'tonne21',
                    'field1':22,
                    'field2':'segundo tres',
                    'id':2
                }
        ],

        'pedido':[
                    {
                    'uni_symb':'tonnedos',
                    'field1':30,
                    'field2':'tresdos',
                    'id':10
                }
        ]
    }

sql =""

for t, r in rcd.items():
    for ea_rcd in r:
        for fn, fv in ea_rcd.items():
            if isinstance(fv, str):
                ea_rcd[fn]='\'' + fv + '\''

    
print (rcd)

for t, r in rcd.items():
    for ea_rcd in r:
        sql = "UPDATE %s SET " %(t)
        for fn, fv in ea_rcd.items():
            if not fn == 'id':
                sql += "%s = %s, " %(fn, fv)
        sql += "WHERE id = %s" %(ea_rcd['id'])
        print (sql)