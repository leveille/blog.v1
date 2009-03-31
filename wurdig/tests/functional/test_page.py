from wurdig.tests import *

class TestPageController(TestController):

    def test_home(self):
        response = self.app.get(url(controller='page', action='home'))
        # Test response...
        
    def test_view(self):
        response = self.app.get(url(controller='page', action='view', slug='about'))
        # assert hasattr(response, 'cache') is True
        assert 'About' in response
        assert 'REQUEST_METHOD' in response.req.environ