# coding utf-8

from modeltranslation.translator import register, TranslationOptions

from . import settings

from wagtail.core.models import Page


@register(Page)
class PageTR(TranslationOptions):
    fields = (
        'title',
        'seo_title',
        'search_description',
    )
    if settings.TRANSLATE_SLUGS:
        fields += (
            'slug',
            'url_path',
        )
