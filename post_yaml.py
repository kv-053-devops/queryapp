import requests
import yaml

# a = input('path: ')
a = """---
symbols:
- APPL
- MSFT
- FB
- AMZN
query_type: realtime"""

b = """---
symbols:
- MSFT
day_range: 1
time_interval: 60
query_type: intraday"""


yaml_src = yaml.load(a,Loader=yaml.FullLoader)
#print(yaml_src)
res = requests.post('http://localhost:5003/query/yml_data',data = b )
print(res.content)

res = requests.post('http://localhost:5003/query/yml_data',data = a )
print(res.content)

# get_response = requests.post('https://api.worldtradingdata.com/api/v1/stock?symbol=AMZN&api_token=0tkx6y1tk3MUvuaNBrye2iIhBACthLoa0gcLHTUSvON2qU7nHKHgmaHMucGn')
# requests.post('https://httpbin.org/post', data={'key':'value'})
# print(get_response.text)
# print(post_resonse.status_code)



