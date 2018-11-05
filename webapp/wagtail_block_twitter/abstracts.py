from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.core.fields import StreamField

from .blocks import TwitterBlock


class MyTwitterPublishAbstract(models.Model):
    twitter_consumer_secret = models.TextField(blank=True, verbose_name=_('Twitter Consumer Secret'))
    twitter_consumer_key = models.TextField(blank=True, verbose_name=_('Twitter Consumer Key'))
    twitter_api_secret = models.TextField(blank=True, verbose_name=_('Twitter Api Secret'))
    twitter_api_key = models.TextField(blank=True, verbose_name=_('Twitter Api Key'))
    twitter_owner = models.TextField(blank=True, verbose_name=_('Twitter Owner'))
    twitter_owner_id = models.TextField(blank=True, verbose_name=_('Twitter Owner Id'))
    twitter_enable_publish = models.BooleanField(default=False,
                                            help_text=_('It will publish entry on twitter account as soon as is saved.'),
                                            verbose_name=_('Enable Twitter Publish'))

    class Meta:
        abstract = True


class MyTwitterBlockAbstract(models.Model):
    twitter = StreamField([('twitter', TwitterBlock()), ], verbose_name=_('Twitter side contents'),
                          null=True, blank=True)

    class Meta:
        abstract = True
