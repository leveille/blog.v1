from wurdig.tests import *

class TestTagController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='tag', action='index'))
        # Test response...
