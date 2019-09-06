from flask import Flask, request, jsonify
import yaml
import requests
import sys
import os
from Querypkg import Query
#from .query_class import Query


# if len(sys.argv) != 1 :
#     app_run_address = sys.argv[1]
#     app_run_port = sys.argv[2]
#     config_api_url = sys.argv[3]
# else:
app_run_address = os.environ.get('APP_ADDRESS', '0.0.0.0')
app_run_port = os.environ.get('APP_PORT', '5003')
config_api_url = os.environ.get('CONFIG_API_URL', 'http://cfgmanapp.dev.svc:5004/conf/query')


app = Flask(__name__)
@app.route("/")
def hello():
    return "There is no service here. Use '/query/yml_data'."

@app.route('/query/yml_data', methods=['POST'])
def receive_yml_data():
    if request.method == 'POST':

        yml_req_src = request.get_data(cache=True, as_text=True)
        yml_data = yaml.load(yml_req_src,Loader=yaml.FullLoader)
        query_obj = Query(yml_data['symbols'],yml_data['query_type'],"http://cfgmanapp.dev.svc:5004/conf/query")

        if query_obj.query_type == 'intraday':
            query_obj.day_range = yml_data['day_range']
            query_obj.time_interval = yml_data['time_interval']

        remote_url = query_obj.url_constructor(query_obj.get_config())
        print (remote_url)
        yml_response = query_obj.make_query(remote_url)

        return yml_response

# @app.route('/conf/query', methods=['GET'])
# def config_data():
#     remote_realtime_api_url = "https://api.worldtradingdata.com"
#     remote_intraday_api_url = "https://intraday.worldtradingdata.com"
#     query_template_realtime = "/api/v1/stock?"
#     query_template_intraday = "/api/v1/intraday?"
#     remote_api_token = "UL0eS95gqeGZMgOtgDW9PZXSuQB9xQex3luk6RhDOErkm74JKch6ps7vXDdQ"
#
#     if request.method == 'GET':
#         query_type = request.args.get('query_type')
#         if query_type == "realtime":
#             response = {"remote_api_url" : remote_realtime_api_url, "query_template" : query_template_realtime, "remote_api_token": remote_api_token }
#             # print (response)
#             return jsonify(response)
#         elif query_type == "intraday" :
#             response = {"remote_api_url" : remote_intraday_api_url, "query_template" : query_template_intraday, "remote_api_token": remote_api_token }
#             # print ("query_type = intraday" )
#             return jsonify(response)
#     return "UNKNOWN QUERY TYPE"


if __name__ == '__main__':
    app.run(host=app_run_address, port=app_run_port)
