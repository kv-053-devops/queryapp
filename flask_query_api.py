from flask import Flask, request, jsonify
import yaml
import requests
import sys
#from .query_class import Query

if len(sys.argv) != 1 :
    app_run_address = sys.argv[1]
    app_run_port = sys.argv[2]
    config_api_url = sys.argv[3]
else:
    app_run_address = "0.0.0.0"
    app_run_port = "5003"
    config_api_url = "http://cfgmanapp.dev.svc:5004/conf/query"

class Query(object):
    def __init__(self,symbols,query_type,day_range = 0,time_interval = 0):
        self.config_api_url = config_api_url
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
            print("UNKNOWN QUERY TYPE")
            return "UNKNOWN QUERY TYPE"

    def get_config(self):
        payload = "query_type=" + self.query_type
        try:
            res = requests.get(self.config_api_url, params=payload)
        except:
            print("Config manager service is not responding")
            return "Config manager service is not responding"
        # print(res.json())
        return res.json()



app = Flask(__name__)
@app.route("/")
def hello():
    return "There is no service here. Use '/query/yml_data'."

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
    app.run(host=app_run_address, port=app_run_port)
