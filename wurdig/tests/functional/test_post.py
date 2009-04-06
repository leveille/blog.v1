from wurdig.tests import *

class TestPostController(TestController):
    def test_archive_missing_year(self):
        response = self.app.get(url(controller='post', action='archive'), status=404)
        
    def test_archive_year_only_2008(self):
        response = self.app.get(url(controller='post', action='archive', year='2008'))
        assert 'Fifth test post' in response
        assert '<p>This is the fifth test post</p>' in response
        assert 'REQUEST_METHOD' in response.req.environ
        
    def test_archive_year_and_month(self):
        response = self.app.get(url(controller='post', 
                                    action='archive', 
                                    year='2009', month='03'))
        assert 'Third test post' in response
        assert '<p>This is the third test post</p>' in response
        assert 'REQUEST_METHOD' in response.req.environ
        
    def test_view(self):
        response = self.app.get(url(controller='post', 
                                    action='view', 
                                    year='2009', 
                                    month='03', slug='third-test-post'))
        # assert hasattr(response, 'cache') is True
        assert 'Third test post' in response
        assert '<p>This is the third test post</p>' in response
        assert 'REQUEST_METHOD' in response.req.environ
                
    def test_view_404_invalid_slug(self):
        response = self.app.get(url(controller='post', 
                                    action='view', 
                                    year='2009', 
                                    month='03', 
                                    slug='foobar'), status=404)