import unittest
from flask_query_api import Query


class TestQuery(unittest.TestCase):

    def setUp(self):
        self.test_realtime_query = Query("AAPL,FB","realtime")
        self.test_intraday_query = Query("AAPL,FB","intraday","2","5")

class TestQueryReturn(TestQuery):
    # def test_object_creation_and_exeption_in_get_config_function(self):
    #     print (self.test_realtime_query.config_api_url)
    #     self.assertEqual(self.test_realtime_query.get_config(),"Config manager service is not responding")
    def test_class_values(self):
        self.assertEqual(self.test_realtime_query.config_api_url, "http://cfgmanapp.dev.svc:5004/conf/query")
        self.assertEqual(self.test_realtime_query.symbols, "AAPL,FB")

if __name__ == '__main__':
    unittest.main()