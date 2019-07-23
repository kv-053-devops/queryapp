from flask import Flask, request, jsonify
import yaml
from query_class import Query


app = Flask(__name__)


@app.route('/query/yml_data', methods=['POST'])
def receive_yml_data():
    if request.method == 'POST':

        yml_req_src = request.get_data(cache=True, as_text=True)
        yml_data = yaml.load(yml_req_src,Loader=yaml.FullLoader)
    #    yaml_from_logic = yaml.dump(yml_data)
    #     print (yml_data)
        query_obj = Query(yml_data['symbols'],yml_data['query_type'])
        # print(query_obj.symbols)
        if query_obj.query_type == 'intraday':
            query_obj.day_range = yml_data['day_range']
            query_obj.time_interval = yml_data['time_interval']

        yml_response = query_obj.make_query()
        print (yml_response)
        return yml_response


@app.route('/conf/query', methods=['GET'])
def config_data():
    remote_realtime_api_url = "https://api.worldtradingdata.com"
    remote_intraday_api_url = "https://intraday.worldtradingdata.com"
    query_template_realtime = "/api/v1/stock?"
    query_template_intraday = "/api/v1/intraday?"
    remote_api_token = "KFzAzKDWU88IAG2uQHp3i3kBa9RCkd3JAWJulicwGNHssxEwq0wElClEUACM"

    if request.method == 'GET':
        query_type = request.args.get('query_type')
        if query_type == "realtime":
            response = {"remote_api_url" : remote_realtime_api_url, "query_template" : query_template_realtime, "remote_api_token": remote_api_token }
            # print (response)
            return jsonify(response)
        elif query_type == "intraday" :
            response = {"remote_api_url" : remote_intraday_api_url, "query_template" : query_template_intraday, "remote_api_token": remote_api_token }
            # print ("query_type = intraday" )
            return jsonify(response)
    return "UNKNOWN QUERY TYPE"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5003')



