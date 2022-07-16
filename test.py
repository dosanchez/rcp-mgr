rcd = {'unitmeas':[{
                    'uni_symb':'tonne11',
                    'field12':12,
                    'field13':'primer tres'
                    },
                 {
                    'uni_symb':'tonne21',
                    'field22':22,
                    'field13':'segundo tres'
                    }],

    'pedido':[{
        'uni_sdos':'tonnedos',
        'field2dos':30,
        'field3dos':'tresdos'
        }]}

# print (a.get('fields'))
# b = a.get('fields')
# print (type(b))
# for k,v in b.items():
#     if isinstance(v, str):
#         b[k]='\'' + v + '\''
#         print(b[k])
    
# print (a.get('fields'))   


for t, r in rcd.items():
    print(t, r)
    for ea_rcd in r:
        print (ea_rcd)
        for fn, fv in ea_rcd.items():
            if isinstance(fv, str):
                ea_rcd[fn]='\'' + fv + '\''
        print(ea_rcd)
    

#value = a.get(table).get(field)
#tam = len(a.get(table))
#print(table, field, value)

#print (tam)
# print(a)
# print(field)
#print(value)