from .models import EntryPage, BlogPage, Category
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
        'excerpt',
    )


@register(EntryPage)
class EntryPageTR(TranslationOptions):
    fields = (
        'excerpt',
        'body',
    )


@register(Category)
class CategoryTR(TranslationOptions):
    fields = (
        'name',
        'description',
    )