import requests, json
import yaml
api_url = "https://api.worldtradingdata.com/api/v1/stock?symbol=AAPL,MSFT,GM,FB,AMZN&api_token=KFzAzKDWU88IAG2uQHp3i3kBa9RCkd3JAWJulicwGNHssxEwq0wElClEUACM"

def get_data_from_remote_api(api_url):
    res = requests.get(api_url)
    # decoded_response = res.decode("UTF-8")
    data = res.json()
    yml_data = yaml.dump(data)
    print(yml_data)
    print(res.status_code)

get_data_from_remote_api(api_url)

# get_response = requests.post('https://api.worldtradingdata.com/api/v1/stock?symbol=AMZN&api_token=0tkx6y1tk3MUvuaNBrye2iIhBACthLoa0gcLHTUSvON2qU7nHKHgmaHMucGn')
# requests.post('https://httpbin.org/post', data={'key':'value'})
# print(get_response.text)
# print(post_resonse.status_code)



