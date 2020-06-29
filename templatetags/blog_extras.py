import re
from django import template
from django.template.defaultfilters import stringfilter

from django.template.defaultfilters import linebreaksbr, urlize, safe

# @register.filter(needs_autoescape=True)
# def urlize_and_linebreaks(text, autoescape=True):
#     return linebreaksbr(
#         urlize(text, autoescape=autoescape),
#         autoescape=autoescape
#     )


register = template.Library()

@register.filter
@stringfilter
def BlogCreateLink(text): # Only one argument.
    """Converts a string contains [[<url link>,<text>]] to hyperlink"""
    # The pattern search for [[ and ]] in between it seperate according to <,> into two groups,
    # The first part is the link while the second is text to display
    pattern = '\[\[(.*?),(.*?)\]\]'
    replacement = r'<a target=”_blank” href=\1>\2</a>'
    result = re.sub(pattern, replacement, text)
    return result

@register.filter
@stringfilter
def BlogCreatefont(text): # Only one argument.
    """Converts a string contains [[<url link>,<text>]] to hyperlink"""
    # The pattern search for [%<tag>%]and create html tag to <tag> 
    
    pattern = '\[%(.*?)%\]'
    replacement = r'<\1>'
    result = re.sub(pattern, replacement, text)
    return result

@register.filter(needs_autoescape=True)
def blog_url_and_linebreaks(text, autoescape=True):
    """ This functionwrap the linebreak and the new url, then call the safe function"""
    return safe(BlogCreatefont(BlogCreateLink(
        linebreaksbr(text,
        autoescape=autoescape))
    ))