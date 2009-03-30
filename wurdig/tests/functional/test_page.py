from wurdig.tests import *

class TestPageController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='page', action='index'))
        # Test response...
