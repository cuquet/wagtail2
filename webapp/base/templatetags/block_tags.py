from datetime import datetime
from django import template
from django.utils.safestring import mark_safe
from wagtail.core.rich_text import RichText, expand_db_html


register = template.Library()


@register.simple_tag(takes_context=False)
def timestamp():
    dt = datetime.now()
    ts = dt.microsecond
    return str(ts)


@register.filter
def mysplit(value, sep="|"):
    parts = value.split(sep)
    return parts[0], sep.join(parts[1:])


@register.filter
def myrichtext(value):
    if isinstance(value, RichText):
        # passing a RichText value through the |richtext filter should have no effect
        return value
    elif value is None:
        html = ''
    else:
        html = expand_db_html(value)

    return mark_safe(html)
