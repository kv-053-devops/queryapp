import requests
import yaml

class Query(object):
    def __init__(self,symbols,query_type,day_range = 0,time_interval = 0,config_api_url):
        self.config_api_url = config_api_url
        self.symbols = symbols
        self.query_type = query_type
        self.day_range = day_range
        self.time_interval = time_interval

    def make_query(self, remote_url):
        res = requests.get(remote_url)
        data = res.json()
        yml_data = yaml.dump(data)
        return yml_data

    # {remote_api_url: ..., query_template: ..., remote_api_token: ...}

    def url_constructor(self, config_data):
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
