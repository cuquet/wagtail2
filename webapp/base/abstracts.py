from django.db import models
from django.utils.translation import ugettext_lazy as _, string_concat

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index

# from .utils import get_image_model_path
from .translation import TranslatedField
from .blocks import BaseStreamBlock, IconPanel, FILTER_CHOICES, SIZE_CHOICES, TabbedPanel


class BaseBodyAbstract(models.Model):
    body = StreamField(BaseStreamBlock(), verbose_name=_('English'), help_text=_('Content'), null=True, blank=True)
    body_ca = StreamField(BaseStreamBlock(), verbose_name=_('Catalan'),
                          help_text=string_concat(_('Content'), ' ', _('Catalan')), null=True, blank=True)
    body_es = StreamField(BaseStreamBlock(), verbose_name=_('Spanish'),
                          help_text=string_concat(_('Content'), ' ', _('Spanish')), null=True, blank=True)

    body_translated = TranslatedField(
        'body',
        'body_ca',
        'body_es',
    )

    search_fields = [
        index.SearchField('body', partial_match=True),
        index.SearchField('body_ca', partial_match=True),
        index.SearchField('body_es', partial_match=True),
    ]

    class Meta:
        abstract = True


class BaseExcerptAbstract(models.Model):
    trans_help_text = _("The page description that will appear under the title."
                        "On Entry list, excerpt to be displayed."
                        "If this field is not filled, a truncate version of body text will be used.")
    excerpt = RichTextField(verbose_name=_('Excerpt'), blank=True,
                            help_text=trans_help_text)
    excerpt_ca = RichTextField(verbose_name=_('Excerpt'), null=True, blank=True,
                               help_text=trans_help_text)
    excerpt_es = RichTextField(verbose_name=_('Excerpt'), null=True, blank=True,
                               help_text=trans_help_text)
    excerpt_translated = TranslatedField(
        'excerpt',
        'excerpt_ca',
        'excerpt_es',
    )
    search_fields = [
        index.SearchField('excerpt', partial_match=True),
        index.SearchField('excerpt_ca', partial_match=True),
        index.SearchField('excerpt_es', partial_match=True),
    ]

    class Meta:
        abstract = True


class BaseMinimalPageAbstract(Page, BaseExcerptAbstract, models.Model):
    title_ca = models.CharField(verbose_name=string_concat(_('Title'), ' ', _('Catalan')), max_length=255, null=True,
                                blank=True)
    title_es = models.CharField(verbose_name=string_concat(_('Title'), ' ', _('Spanish')), max_length=255, null=True,
                                blank=True)
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

    title_translated = TranslatedField(
        'title',
        'title_ca',
        'title_es',
    )

    content_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                ImageChooserPanel('header_image', classname="col6"),
                MultiFieldPanel([
                    FieldPanel('parallax_filter', classname=""),
                    FieldPanel('parallax_size', classname=""),
                    ], classname="col6")
            ]),
            TabbedPanel([
                MultiFieldPanel([
                    FieldPanel('title'),
                    FieldPanel('excerpt'),
                ], heading=_("English"), classname=""),
                MultiFieldPanel([
                    FieldPanel('title_ca'),
                    FieldPanel('excerpt_ca'),
                ], heading=_("Catalan")),
                MultiFieldPanel([
                    FieldPanel('title_es'),
                    FieldPanel('excerpt_es'),
                ], heading=_("Spanish"))
            ])
        ], heading=_("Header"), classname="collapsible")]

    promote_panels = Page.promote_panels + []

    settings_panels = Page.settings_panels + [
        IconPanel('menu_icon'),
        FieldPanel('show_search'),
    ]

    class Meta:
        abstract = True


class BasePageAbstrac(BaseMinimalPageAbstract, BaseBodyAbstract):

    search_fields = BaseMinimalPageAbstract.search_fields + BaseBodyAbstract.search_fields

    content_panels = BaseMinimalPageAbstract.content_panels + [
                MultiFieldPanel([
                    TabbedPanel([
                        StreamFieldPanel('body', heading=_("English"), classname="full"),
                        StreamFieldPanel('body_ca', heading=_("Catalan"), classname="full"),
                        StreamFieldPanel('body_es', heading=_("Spanish"), classname="full"),
                    ])
                ], heading=_("Content"), classname="collapsible"),
    ]

    promote_panels = BaseMinimalPageAbstract.promote_panels

    class Meta:
        abstract = True

