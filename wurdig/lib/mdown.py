from webhelpers.html.converters import markdown

__all__ = ['mdown']

def mdown(content):
    return content
    return markdown(content, safe_mode="remove")