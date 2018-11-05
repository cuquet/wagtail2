from .models import HomePage, StandardPage, HomePageCard, HomePageRelatedLink, StandardPageRelatedLink
from modeltranslation.translator import register, TranslationOptions
# from modeltranslation.decorators import register


@register(HomePageCard)
class CardTR(TranslationOptions):
    fields = (
        'title',
        'text',
        'footer',
    )


@register(HomePageRelatedLink)
class HomePageRelatedLinkTR(TranslationOptions):
    fields = (
        'title',
    )


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = (
        'excerpt',
        # 'card_items',
        # 'related_links',
    )


@register(StandardPageRelatedLink)
class StandardPageRelatedLinkTR(TranslationOptions):
    fields = (
        'title',
    )


@register(StandardPage)
class StandardPageTR(TranslationOptions):
    fields = (
        'excerpt',
        'body',
    )
