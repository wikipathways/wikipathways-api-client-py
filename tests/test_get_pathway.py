import unittest
from collections import namedtuple
from mock import MagicMock
from mock import patch
from wikipathways_api_client import WikipathwaysApiClient

class TestSimple(unittest.TestCase):

    def test_request_get(self):
        with patch('requests.get') as patched_get:
            expected_text = open('./WP2062.xml', 'r').read()
            ReturnValue = namedtuple('ReturnValue', 'text')
            patched_get.return_value = ReturnValue(text=expected_text)
            wikipathways_api_client_instance = WikipathwaysApiClient()

            # Get pathway with desired file format
            kwargs = {
                'identifier': 'WP2062',
                'version': 0,
                'file_format': 'application/vnd.gpml+xml'
            }
            wikipathways_api_client_instance.get_pathway_as(**kwargs)
            patched_get.assert_called_once_with('http://webservice.wikipathways.org/getPathwayAs', params={'fileType': 'gpml', 'pwId': 'WP2062', 'revision': 0})
    
    '''
    def test_failure(self):
        self.assertTrue(False)
    '''

if __name__ == '__main__':
    unittest.main()
