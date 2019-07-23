import requests
import yaml

# a = input('path: ')
a = {"symbol":"MSFT,GOOG"}

#print(yaml_src)
res = requests.put('http://localhost:5004/save',json = a )
print(res.content)
print(res)