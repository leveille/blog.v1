from tidylib import tidy_fragment

__all__ = ['mytidy']

def mytidy(content):
    BASE_OPTIONS = {
        "output-xhtml": 0,     # XHTML instead of HTML4
        "indent": 1,           # Pretty; not too much of a performance hit
        "indent-spaces":4,
        "tab-size":4,
        "tidy-mark": 0,        # No tidy meta tag in output
        "wrap": 0,             # No wrapping
        "alt-text": "",        # Help ensure validation
        "doctype": 'strict',   # Little sense in transitional for tool-generated markup...
        "force-output": 1,     # May not get what you expect but you will get something
        "char-encoding":'utf8',
        "input-encoding":'utf8',
        "output-encoding":'utf8',
        }
    content = tidy_fragment(content, BASE_OPTIONS)
    return content[0]