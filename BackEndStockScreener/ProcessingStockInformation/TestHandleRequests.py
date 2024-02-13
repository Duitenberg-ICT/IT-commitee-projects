import unittest
import sys
import os
script_dir = os.path.dirname(__file__)  # Gets the directory where the script is located.
project_root = os.path.join(script_dir, '..', '..', '..')  # Navigate up to the project root.
sys.path.append(os.path.abspath(project_root))
from BackEndStockScreener.ProcessingStockInformation.handleRequests import app
class FlaskAppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_filtered_parameter_data(self):
        # Test without any query parameters (should use defaults)
        response = self.app.get('/get_filtered-parameter_data')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIsInstance(data, list)  # Assuming the response is a list of items

        # Test with specific query parameters
        response = self.app.get('/get_filtered-parameter_data?key=profitMargins&min=0.1&max=0.5&top_percentile=50')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # Further tests can be added here to validate that the data matches the expected filtered results.
        # This would depend on the test data available within the StockScreener instance during testing.

   
