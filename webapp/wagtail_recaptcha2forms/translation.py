from .models import FormPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(FormPage)
class FormPageTR(TranslationOptions):
    fields = (
        'excerpt',
        'thank_you_text',
    )
