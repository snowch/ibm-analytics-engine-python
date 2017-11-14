from unittest import TestCase


from ibm_analytics_engine import CloudFoundryAPI

class TestCloudFoundryAPI(TestCase):
    def test_api_key_file_is_accessed(self):
        try:
            error_class = IOError
        except:
            error_class = FileNotFoundError

        with self.assertRaises(error_class):
            cf = CloudFoundryAPI(api_key_filename='does_not_exist')
