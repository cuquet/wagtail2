from django.conf import settings

from wagtail.admin.edit_handlers import BaseFormEditHandler


class TabbedPanel(BaseFormEditHandler):
    template = "wagtail_modeltranslation/edit_handlers/tabbed_panel.html"

    def __init__(self, children=(), *args, **kwargs):
        self.base_form_class = kwargs.pop('base_form_class', None)
        super(TabbedPanel, self).__init__(*args, **kwargs)
        self.children = children

    def clone(self):
        new = super(TabbedPanel, self).clone()
        new.base_form_class = self.base_form_class
        new.lang_list = settings.LANGUAGES
        return new
