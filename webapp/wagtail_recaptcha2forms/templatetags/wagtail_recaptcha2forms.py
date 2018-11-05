from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def recaptcha_key():
    return settings.RECAPTCHA_PUBLIC_KEY


@register.inclusion_tag('wagtail_recaptcha2forms/tags/recaptcha_init.html', takes_context=True)
def recaptcha_init(context, language=None, explicit=False):
    return {
        'explicit': explicit,
        'language': language,
        'request': context['request'],
    }


@register.inclusion_tag('wagtail_recaptcha2forms/tags/recaptcha_init.html')
def recaptcha_explicit_init(language=None):
    return {'explicit': True, 'language': language}

