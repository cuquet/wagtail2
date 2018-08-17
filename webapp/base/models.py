from __future__ import unicode_literals

from django.db import models
from django import forms

from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractForm

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable, Collection
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import PageChooserPanel, FieldPanel, FieldRowPanel, \
    MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from .abstracts import BasePageAbstrac, BaseMinimalPageAbstract
from .blocks import CARD_CHOICES, BaseStreamBlock, BaseParallaxBlock

from webapp.twitter.abstracts import MyTwitterBlockAbstract
from webapp.twitter.panels import twitter_block_panel
from webapp.blog.models import Category

# http://docs.wagtail.io/en/v2.1/reference/contrib/settings.html?highlight=settings
@register_setting(icon='cogs')
class BaseSiteSettings(BaseSetting):
    num_results_page = models.IntegerField(default=5, verbose_name=_('Results per page on search'))
    google_analytics_id = models.CharField(blank=True, max_length=50,
                                           help_text=_("Google Analytics ID (http://www.google.com/analytics/)"))
    contact_us = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        verbose_name=_('Internal link to contact us page'),
        help_text=_('Choose an existing page if you want the link to point somewhere inside the CMS.')
    )

    class Meta:
        verbose_name = _('Various settings')


# A couple of abstract classes that contain commonly used fields
class LinkFields(models.Model):
    link_external = models.URLField(
        "External link",
        blank=True,
        null=True,
        help_text=_('Set an external link if you want the link to point somewhere outside the CMS.')
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text=_('Choose an existing page if you want the link to point somewhere inside the CMS.')
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='+',
        help_text=_('Choose an existing document if you want the link to open a document.')
    )
    link_category = models.ForeignKey(Category,
                                      null=True,
                                      blank=True,
                                      related_name="+",
                                      verbose_name=_('Blog Category'),
                                      on_delete=models.SET_NULL)

    @property
    def link(self):
        if self.link_page:
            return self.link_page
        elif self.link_document:
            return self.link_document
        elif self.link_category:
            return "blog/category/" + self.link_category.slug
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
        # SnippetChooserPanel('link_category'),
        FieldPanel('link_category'),
    ]


class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels),
    ]


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    site_tags.py
    """
    rawhtml = models.CharField(default=' ', max_length=255,
                               help_text=_('A text area for entering raw HTML which will '
                                           'be rendered unescaped in the page output.') )

    panels = [
        FieldPanel('rawhtml',widget=forms.Textarea),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = _('Footer Text')


class CardContent(models.Model):
    url_link = models.CharField(
        verbose_name=_('Url'),
        max_length=255,
        null = True, blank = True,
        help_text=_("Relative links are allowed")
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_("Title of the card")
    )
    text = RichTextField(verbose_name="Text", null=True, blank=True)
    footer = RichTextField(verbose_name="Footer", null=True, blank=True)

    panels = [
        FieldPanel('url_link'),
        FieldPanel('title'),
        FieldPanel('text', classname=''),
        FieldPanel('footer', classname='collapsible'),
    ]

    class Meta:
        abstract = True


class Card(CardContent):
    image = models.ForeignKey('wagtailimages.Image', verbose_name=_('Header image'),
                              null=True, blank=True,
                              on_delete=models.SET_NULL, related_name='+')
    card_type = models.CharField(verbose_name=_('Card type'), max_length=30, choices=CARD_CHOICES,
                                     default="", help_text=_('Check on components page'),
                                     null=True, blank=True)
    panels = [
        FieldPanel('card_type', classname=""),
        ImageChooserPanel('image', classname=""),
        MultiFieldPanel(CardContent.panels, classname=""),
    ]


class HomePage(BaseMinimalPageAbstract):
    search_fields = BaseMinimalPageAbstract.search_fields

    content_panels = BaseMinimalPageAbstract.content_panels + [
        MultiFieldPanel([
            InlinePanel('card_items', label=_("Card items"), # help_text=_(""),
                min_num=None, max_num=None, classname=""),
        ], heading=_('Cards'), classname="collapsible"),
        MultiFieldPanel([
            InlinePanel('related_links', label=_('Related links')),
        ], heading=_('Related links'), classname="collapsible"),
    ]

    promote_panels = BaseMinimalPageAbstract.promote_panels

    settings_panels = BaseMinimalPageAbstract.settings_panels

    # Defining what content type can sit under the parent. Since it's a blank
    # array no subpage can be added
    # subpage_types = []

    # @property
    # def cards(self):
    #     return [card for card in self.card_items.all()]

    class Meta:
        verbose_name = _('Homepage')


class HomePageCard(Card, Orderable ):
    card_items = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='card_items')


class HomePageRelatedLink(RelatedLink, Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='related_links')


class StandardPage(MyTwitterBlockAbstract, BasePageAbstrac):
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = BasePageAbstrac.search_fields

    content_panels = BasePageAbstrac.content_panels + [
        MultiFieldPanel([
            # InlinePanel('carousel_items', label="Carousel items"),
            InlinePanel('related_links', label=_('Related links')),
            ImageChooserPanel('feed_image'),
        ], heading=_('Related links and feed image'), classname="collapsible"),
        ] + twitter_block_panel

    promote_panels = BasePageAbstrac.promote_panels


class StandardPageRelatedLink(RelatedLink, Orderable):
    page = ParentalKey(StandardPage, on_delete=models.CASCADE, related_name='related_links')
