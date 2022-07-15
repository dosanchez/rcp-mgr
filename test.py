a = {'unitmeas':{'uni_symb':'tonne', 'field2': 5, 'field3': 'hola'}, }

print (a.get('fields'))
b = a.get('fields')
print (type(b))
for k,v in b.items():
    if isinstance(v, str):
        b[k]='\'' + v + '\''
        print(b[k])
    
print (a.get('fields'))   