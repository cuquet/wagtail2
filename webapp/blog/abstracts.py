import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

from modelcluster.contrib.taggit import ClusterTaggableManager

from webapp.base.abstracts import BaseMinimalPageAbstract
from webapp.base.translation import TranslatedField
from webapp.base.blocks import TabbedPanel

from .utils import get_image_model_path


class EntryAbstract(BaseMinimalPageAbstract, models.Model):
    body = RichTextField(verbose_name=_('Content'))
    body_ca = RichTextField(verbose_name=_('Content'), null=True, blank=True)
    body_es = RichTextField(verbose_name=_('Content'), null=True, blank=True)
    tags = ClusterTaggableManager(through='blog.TagEntryPage', blank=True)
    date = models.DateTimeField(verbose_name=_("Post date"), default=datetime.datetime.today)
    categories = models.ManyToManyField('blog.Category', through='blog.CategoryEntryPage', blank=True)
    num_comments = models.IntegerField(default=0, editable=False)

    body_translated = TranslatedField(
        'body',
        'body_ca',
        'body_es',
    )

    search_fields = BaseMinimalPageAbstract.search_fields + [
        index.SearchField('body', partial_match=True),
        index.SearchField('body_ca', partial_match=True),
        index.SearchField('body_es', partial_match=True),
    ]

    content_panels = BaseMinimalPageAbstract.content_panels + [
        MultiFieldPanel([
                TabbedPanel([
                    MultiFieldPanel([
                        FieldPanel('body', classname="full"),
                    ], heading=_("English"), classname="full"),
                    MultiFieldPanel([
                        FieldPanel('body_ca', classname="full"),
                    ], heading=_("Catalan")),
                    MultiFieldPanel([
                        FieldPanel('body_es', classname="full"),
                    ], heading=_("Spanish"))
                ])
            ],
            heading=_('Content'), classname="collapsible collapsed"
        ),
        MultiFieldPanel([
                FieldPanel('tags'),
                InlinePanel('entry_categories', label=_("Categories")),
                InlinePanel(
                    'related_entrypage_from',
                    label=_("Related Entries"),
                    panels=[PageChooserPanel('entrypage_to')]
                ),
            ],
            heading=_("Metadata")),
    ]

    settings_panels = [FieldPanel('date')] + BaseMinimalPageAbstract.settings_panels

    class Meta:
        abstract = True
