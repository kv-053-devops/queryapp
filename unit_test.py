import unittest
import json
from Querypkg import Query

class TestQuery(unittest.TestCase):

    def setUp(self):
        self.test_realtime_query = Query(["AAPL","FB"],"realtime","http://cfgmanapp.dev.svc:5004/conf/query")
        self.test_intraday_query = Query(["AAPL"],"intraday","http://cfgmanapp.dev.svc:5004/conf/query","2","60")

class TestQueryReturn(TestQuery):
    # def test_object_creation_and_exeption_in_get_config_function(self):
    #     print (self.test_realtime_query.config_api_url)
    #     self.assertEqual(self.test_realtime_query.get_config(),"Config manager service is not responding")
    def test_class_config_api_url_value(self):
        self.assertEqual(self.test_realtime_query.config_api_url, "http://cfgmanapp.dev.svc:5004/conf/query")

    def test_realtime_class_symbols_value(self):
        self.assertEqual(self.test_realtime_query.symbols, ["AAPL","FB"])

    def test_intraday_class_symbols_value(self):
        self.assertEqual(self.test_intraday_query.symbols, ["AAPL"])

    def test_url_realtime_construction_function(self):
        self.assertEqual(self.test_realtime_query.url_constructor({"remote_api_url":"https://api.worldtradingdata.com",
            "query_template":"/api/v1/stock?","remote_api_token":"UL0eS95gqeGZMgOtgDW9PZXSuQB9xQex3luk6RhDOErkm74JKch6ps7vXDdQ"}),
            "https://api.worldtradingdata.com/api/v1/stock?symbol=AAPL,FB&api_token=UL0eS95gqeGZMgOtgDW9PZXSuQB9xQex3luk6RhDOErkm74JKch6ps7vXDdQ")

    def test_url_intraday_construction_function(self):
        self.assertEqual(self.test_intraday_query.url_constructor({"remote_api_url": "https://intraday.worldtradingdata.com",
            "query_template": "/api/v1/intraday?",
            "remote_api_token": "UL0eS95gqeGZMgOtgDW9PZXSuQB9xQex3luk6RhDOErkm74JKch6ps7vXDdQ"}),
            "https://intraday.worldtradingdata.com/api/v1/intraday?symbol=AAPL&interval=60&range=2&api_token=UL0eS95gqeGZMgOtgDW9PZXSuQB9xQex3luk6RhDOErkm74JKch6ps7vXDdQ")

if __name__ == '__main__':
    unittest.main()
