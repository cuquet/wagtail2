import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField

from modelcluster.contrib.taggit import ClusterTaggableManager

from webapp.base.abstracts import BaseMinimalPageAbstract

from .utils import get_image_model_path


class EntryAbstract(BaseMinimalPageAbstract, models.Model):
    body = RichTextField(verbose_name=_('Body'))
    tags = ClusterTaggableManager(through='blog.TagEntryPage', blank=True)
    date = models.DateTimeField(verbose_name=_("Post date"), default=datetime.datetime.today)
    categories = models.ManyToManyField('blog.Category', through='blog.CategoryEntryPage', blank=True)
    num_comments = models.IntegerField(default=0, editable=False)

    content_panels = BaseMinimalPageAbstract.content_panels + [
        MultiFieldPanel([
                FieldPanel('body', classname="full"),
            ],
            heading=_('Content')
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
