from webhelpers.html.converters import markdown

__all__ = ['mdown', 'nl2br']

def mdown(content, mode="remove"):
    """
    Options for mode include (escape, replace, remove)
    """
    return markdown(content, safe_mode=mode)

def nl2br(content):
    return '<br>'.join(content.split('\n'))