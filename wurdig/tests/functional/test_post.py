from wurdig.tests import *

class TestPostController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='post', action='index'))
        # Test response...
