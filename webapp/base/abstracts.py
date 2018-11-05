from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index

# from .utils import get_image_model_path
# from webapp import TranslatedField
from .blocks import BaseStreamBlock, IconPanel, FILTER_CHOICES, SIZE_CHOICES  # , TabbedPanel


class BaseBodyAbstract(models.Model):
    body = StreamField(BaseStreamBlock(), help_text=_('Streamfield Content'), null=True, blank=True)

    search_fields = [
        index.SearchField('body', partial_match=True),
    ]

    class Meta:
        abstract = True


class BaseExcerptAbstract(models.Model):
    trans_help_text = _("The page description that will appear under the title."
                        "On Entry list, excerpt to be displayed."
                        "If this field is not filled, a truncate version of body text will be used.")
    excerpt = RichTextField(verbose_name=_('Excerpt'), blank=True,
                            help_text=trans_help_text)
    search_fields = [
        index.SearchField('excerpt', partial_match=True),
    ]

    class Meta:
        abstract = True


class BaseMinimalPageAbstract(Page, BaseExcerptAbstract, models.Model):
    header_image = models.ForeignKey('wagtailimages.Image', verbose_name=_('Header image'), null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+')

    parallax_filter = models.CharField(verbose_name=_('Image Filter'), max_length=30, choices=FILTER_CHOICES,
                                       default="filter-black", help_text=_('Filter effect'),
                                       null=True, blank=True)
    parallax_size = models.CharField(verbose_name=_('Image Size'), max_length=30, choices=SIZE_CHOICES,
                                     default="parallax-small", help_text=_('Size effect'),
                                     null=True, blank=True)
    show_search = models.BooleanField(
        verbose_name=_('Show search in menus'),
        default=False,
        help_text=_('Whether a search form will appear in automatically generated menus')
    )
    menu_icon = models.CharField(verbose_name='Icon Class', max_length=60, null=True, blank=True)

    search_fields = Page.search_fields + BaseExcerptAbstract.search_fields

    content_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                ImageChooserPanel('header_image', classname="col6"),
                MultiFieldPanel([
                    FieldPanel('parallax_filter', classname=""),
                    FieldPanel('parallax_size', classname=""),
                    ], classname="col6")
            ]),
            FieldPanel('title', classname="title"),
            FieldPanel('excerpt', classname="full"),
        ], heading=_("Header"), classname="collapsible")]

    promote_panels = Page.promote_panels

    settings_panels = Page.settings_panels + [
        IconPanel('menu_icon'),
        FieldPanel('show_search'),
    ]

    class Meta:
        abstract = True


class BasePageAbstract(BaseMinimalPageAbstract, BaseBodyAbstract):

    search_fields = BaseMinimalPageAbstract.search_fields + BaseBodyAbstract.search_fields

    content_panels = BaseMinimalPageAbstract.content_panels + [
        MultiFieldPanel([StreamFieldPanel('body')], heading=_("Content"), classname="collapsible"),
    ]

    promote_panels = BaseMinimalPageAbstract.promote_panels

    settings_panels = BaseMinimalPageAbstract.settings_panels

    class Meta:
        abstract = True

