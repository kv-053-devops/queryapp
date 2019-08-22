from flask import Flask, request, jsonify
import yaml
from query_class import Query

if len(sys.argv) != 1 :
    app_run_address = sys.argv[1]
    app_run_port = sys.argv[2]
    config_api_url = sys.argv[3]
else:
    app_run_address = '0.0.0.0'
    app_run_port = '5003'
    config_api_url = "http://127.0.0.1:5004/conf/query"

app = Flask(__name__)
@app.route("/")
def hello():
    return "The root uri '/' doesn't configured. Use '/logic/query_data' instead."

@app.route('/query/yml_data', methods=['POST'])
def receive_yml_data():
    if request.method == 'POST':

        yml_req_src = request.get_data(cache=True, as_text=True)
        yml_data = yaml.load(yml_req_src,Loader=yaml.FullLoader)
        query_obj = Query(config_api_url,yml_data['symbols'],yml_data['query_type'])
        if query_obj.query_type == 'intraday':
            query_obj.day_range = yml_data['day_range']
            query_obj.time_interval = yml_data['time_interval']

        yml_response = query_obj.make_query()

        return yml_response

if __name__ == "__main__":
    app.run(host=app_run_address, port=app_run_port)

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port='5003')



