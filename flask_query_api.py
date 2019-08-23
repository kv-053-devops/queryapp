from flask import Flask, request, jsonify
import yaml
import requests
#from .query_class import Query


app = Flask(__name__)


@app.route('/query/yml_data', methods=['POST'])
def receive_yml_data():
    if request.method == 'POST':

        yml_req_src = request.get_data(cache=True, as_text=True)
        yml_data = yaml.load(yml_req_src,Loader=yaml.FullLoader)
        query_obj = Query(yml_data['symbols'],yml_data['query_type'])
        if query_obj.query_type == 'intraday':
            query_obj.day_range = yml_data['day_range']
            query_obj.time_interval = yml_data['time_interval']

        yml_response = query_obj.make_query()

        return yml_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5003')

class Query(object):
    def __init__(self,symbols,query_type,day_range = 0,time_interval = 0):
        self.config_api_url = "http://cfgmanapp.dev.svc:5004/conf/query"
        self.symbols = symbols
        self.query_type = query_type
        self.day_range = day_range
        self.time_interval = time_interval

    def make_query(self):
        res = requests.get(self.url_constructor())
        data = res.json()
        yml_data = yaml.dump(data)
        return yml_data

    # {remote_api_url: ..., query_template: ..., remote_api_token: ...}

    def url_constructor(self):
        config_data = self.get_config()
        if self.query_type == 'realtime':
            api_url = config_data["remote_api_url"] + config_data["query_template"] + 'symbol=' + ','.join(self.symbols) + "&api_token=" + config_data["remote_api_token"]
            return api_url
        elif self.query_type == 'intraday':
            api_url = config_data["remote_api_url"] + config_data["query_template"] + 'symbol=' + "".join(self.symbols) +  "&interval=" + str(self.time_interval) + "&range=" + str(self.day_range) +"&api_token=" + config_data["remote_api_token"]
            return api_url
        else:
            return 'UNKNOWN QUERY TYPE'

    def get_config(self):
        payload = "query_type=" + self.query_type
        res = requests.get(self.config_api_url, params=payload)
        # print(res.json())
        return res.json()

