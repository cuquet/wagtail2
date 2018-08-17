import os

from django.db import models
from django.shortcuts import render

from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractForm
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, \
    MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel

from .forms import WagtailCaptchaFormBuilder, remove_captcha_field

from webapp.base.abstracts import BaseMinimalPageAbstract
from webapp.base.blocks import FILTER_CHOICES


class WagtailCaptchaEmailForm(AbstractEmailForm):
    """A WagtailCaptchaEmailForm Page. Pages implementing a captcha form with email  should inhert from it"""
    # is_abstract = True  # Don't display me in "Add"

    form_builder = WagtailCaptchaFormBuilder

    def process_form_submission(self, form):
        remove_captcha_field(form)
        return super(WagtailCaptchaEmailForm, self).process_form_submission(form)

    class Meta:
        abstract = True


class WagtailCaptchaForm(AbstractForm):
    """A WagtailCaptchaForm Page. Pages implementing a captcha form should inhert from it"""
    # is_abstract = True  # Don't display me in "Add"

    form_builder = WagtailCaptchaFormBuilder

    def process_form_submission(self, form):
        remove_captcha_field(form)
        return super(WagtailCaptchaForm, self).process_form_submission(form)

    class Meta:
        abstract = True


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(WagtailCaptchaEmailForm, BaseMinimalPageAbstract):
    thank_you_text = RichTextField(blank=True)

    is_modal = models.BooleanField(
        verbose_name=_('Must be modal form'),
        default=False,
        help_text=_('Check it if you want to launch view as modal')
    )

    search_fields = BaseMinimalPageAbstract.search_fields

    content_panels = [ FormSubmissionsPanel(), ] + BaseMinimalPageAbstract.content_panels + \
                     [ InlinePanel('form_fields', label=_('Form fields')),
                       MultiFieldPanel([
                           FieldRowPanel([
                                FieldPanel('from_address', classname="col6"),
                                FieldPanel('to_address', classname="col6"),
                            ]),
                            FieldPanel('subject'),
                            FieldPanel('thank_you_text', classname="full"),
                        ], heading=_("Email"), classname="collapsible collapsed")
                    ]

    promote_panels = BaseMinimalPageAbstract.promote_panels

    def serve(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
                split = self.template.split('.html')
                split[-1] = '_modal'
                split.append('.html')
                self.ajax_template = ''.join(split)
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)

                if request.is_ajax():
                    self.template = self.ajax_template
                    name, ext = os.path.splitext(self.template)
                    self.landing_page_template = name + '_landing' + ext
                else:
                    self.landing_page_template = self.get_landing_page_template(request)
                # render the landing_page
                # TODO: It is much better to redirect to it
                return render(
                    request,
                    self.landing_page_template,
                    self.get_context(request)
                )
        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        return render(
            request,
            self.get_template(request),
            context
        )
