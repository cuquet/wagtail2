# coding: utf-8

import re
from datetime import datetime
from six import iteritems

from django import template
from django.utils.translation import activate, get_language, get_language_info
try:
    from django.core.urlresolvers import resolve
except ImportError:
    from django.urls import resolve

from modeltranslation import settings as mt_settings
from modeltranslation.settings import DEFAULT_LANGUAGE

from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl

from ..contextlib import use_language

register = template.Library()


# TODO: check templatetag usage

@register.simple_tag(takes_context=False)
def timestamp():
    dt = datetime.now()
    ts = dt.microsecond
    return str(ts)


# CHANGE LANGUAGE
@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    current_language = get_language()

    if 'request' in context and lang and current_language:
        request = context['request']
        match = resolve(request.path)
        non_prefixed_path = re.sub(current_language + '/', '', request.path, count=1)

        # means that is an wagtail page object
        if match.url_name == 'wagtail_serve':
            path_components = [component for component in non_prefixed_path.split('/') if component]
            page, args, kwargs = request.site.root_page.specific.route(request, path_components)

            activate(lang)
            translated_url = page.url
            activate(current_language)

            return translated_url
        elif match.url_name == 'wagtailsearch_search':
            path_components = [component for component in non_prefixed_path.split('/') if component]

            translated_url = '/' + lang + '/' + path_components[0] + '/'
            if request.GET:
                translated_url += '?'
                for count, (key, value) in enumerate(iteritems(request.GET)):
                    if count != 0:
                        translated_url += "&"
                    translated_url += key + '=' + value
            return translated_url

    return ''


# class GetAvailableLanguagesNode(template.Node):
#     """Get available languages."""
#
#     def __init__(self, variable):
#         self.variable = variable
#
#     def render(self, context):
#         """Rendering."""
#         context[self.variable] = mt_settings.AVAILABLE_LANGUAGES
#         return ''


# Alternative to slugurl which uses chosen or default language for language
@register.simple_tag(takes_context=True)
def slugurl_trans(context, slug, language=None):
    """
    Examples:
        {% slugurl_trans 'default_lang_slug' %}
        {% slugurl_trans 'de_lang_slug' 'de' %}

    Returns the URL for the page that has the given slug.
    """
    language = language or DEFAULT_LANGUAGE

    with use_language(language):
        page = Page.objects.filter(slug=slug).first()

    if page:
        # call pageurl() instead of page.relative_url() here so we get the ``accepts_kwarg`` logic
        return pageurl(context, page)


# @register.tag('get_available_languages_wmt')
# def do_get_available_languages(unused_parser, token):
#     """
#     Store a list of available languages in the context.
#
#     Usage::
#
#         {% get_available_languages_wmt as languages %}
#         {% for language in languages %}
#         ...
#         {% endfor %}
#
#     This will just pull the MODELTRANSLATION_LANGUAGES (or LANGUAGES) setting
#     from your setting file (or the default settings) and
#     put it into the named variable.
#     """
#     args = token.contents.split()
#     if len(args) != 3 or args[1] != 'as':
#         raise template.TemplateSyntaxError(
#             "'get_available_languages_wmt' requires 'as variable' "
#             "(got %r)" % args)
#     return GetAvailableLanguagesNode(args[2])
@register.inclusion_tag('wagtail_modeltranslation/tags/menu_dropdown_language.html', takes_context=True)
def lang_top_menu(context):
    pass
    return {'request': context['request'],}


@register.inclusion_tag('wagtail_modeltranslation/tags/language_selector.html', takes_context=True)
def lang_selector(context):
    pass
    return {'request': context['request'],}
