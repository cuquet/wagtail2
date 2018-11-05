from __future__ import absolute_import, unicode_literals

from wagtail.contrib.forms.forms import FormBuilder
from .fields import ReCaptchaField
from .widgets import ReCaptchaWidget


class WagtailCaptchaFormBuilder(FormBuilder):
    CAPTCHA_FIELD_NAME = 'recaptcha'

    @property
    def formfields(self):
        # Add wagtailcaptcha to formfields property
        fields = super(WagtailCaptchaFormBuilder, self).formfields
        fields[WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME] = ReCaptchaField(widget=ReCaptchaWidget())

        return fields


def remove_captcha_field(form):
    form.fields.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
    form.cleaned_data.pop(WagtailCaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
