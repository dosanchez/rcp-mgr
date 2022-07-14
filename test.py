a = {'table':'unitmeas','fields':{'uni_symb':'tonne'}}
print (type(a.get('fields')))
b = a.get('fields')
print (type(b))
for k,v in b.items():
    print(k, v)