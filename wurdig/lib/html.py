"""http://code.google.com/p/soclone/source/browse/trunk/soclone/utils/html.py"""
"""Utilities for working with HTML."""
import html5lib
from html5lib import sanitizer, serializer, tokenizer, treebuilders, treewalkers

__all__ = ['sanitize_html']

class HTMLSanitizerMixin(sanitizer.HTMLSanitizerMixin):
    acceptable_elements = ('a', 'em', 'blockquote', 'p', 'br', 'ul', 'ol', 'li', 'b', 'strong', 'i', 'em')
    acceptable_attributes = ('href', 'title')

    allowed_elements = acceptable_elements
    allowed_attributes = acceptable_attributes
    allowed_css_properties = ()
    allowed_css_keywords = ()
    allowed_svg_properties = ()

class HTMLSanitizer(tokenizer.HTMLTokenizer, HTMLSanitizerMixin):
    def __init__(self, stream, encoding=None, parseMeta=True, useChardet=True,
                 lowercaseElementName=True, lowercaseAttrName=True):
        tokenizer.HTMLTokenizer.__init__(self, stream, encoding, parseMeta,
                                         useChardet, lowercaseElementName,
                                         lowercaseAttrName)

    def __iter__(self):
        for token in tokenizer.HTMLTokenizer.__iter__(self):
            token = self.sanitize_token(token)
            if token:
                yield token

def sanitize_html(html):
    """Sanitizes an HTML fragment."""
    p = html5lib.HTMLParser(tokenizer=HTMLSanitizer,
                            tree=treebuilders.getTreeBuilder("dom"))
    dom_tree = p.parseFragment(html)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.HTMLSerializer(omit_optional_tags=False,
                                  quote_attr_values=True)
    output_generator = s.serialize(stream)
    return u''.join(output_generator)
