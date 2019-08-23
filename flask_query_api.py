from flask import Flask, request, jsonify
import yaml
from . query_class import Query


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



