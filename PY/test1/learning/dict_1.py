dict1={'name':'lmq','age':'23','sex':'nan','tel':{1:'11111',2:'2222222',3:'3333333'}}
k=list(dict1.keys())[0]
print(dict1.get(k))
print(isinstance(dict1.get(k),dict))