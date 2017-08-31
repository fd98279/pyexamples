import unittest,logging
from rackindexer import core
logger = logging.getLogger()

class TestCore(unittest.TestCase):

    def test_parse_blob_cache_not_empty(self):
        '''
            Test parse cache is not empty
        '''
        parser = core.parser(logger)
        parser.parse_blob("a|b")
        self.assertNotEqual(parser.cache, None)

    def test_parse_blob_cache_value(self):
        '''
            Test parse cache value
        '''
        parser = core.parser(logger)
        parser.parse_blob("a|b")
        self.assertNotEqual(parser.cache['a'], None)
        self.assertNotEqual(parser.cache['b'], None)
        self.assertEqual(parser.cache['c'], None)
