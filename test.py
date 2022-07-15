a = {'unitmeas':{'uni_symb':'tonne','field2':15,'field3':'tres'},'unitdos':{'uni_sdos':'tonnedos','field2dos':30,'field3dos':'tresdos'}}

# print (a.get('fields'))
# b = a.get('fields')
# print (type(b))
# for k,v in b.items():
#     if isinstance(v, str):
#         b[k]='\'' + v + '\''
#         print(b[k])
    
# print (a.get('fields'))   


for k, v in a.items():
    for fk, fv in v.items():
        if isinstance(fv, str):
            v[fk]='\'' + fv + '\''

#value = a.get(table).get(field)
#tam = len(a.get(table))
#print(table, field, value)

#print (tam)
print(a)
# print(field)
#print(value)