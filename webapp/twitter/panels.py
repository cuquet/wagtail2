from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel)
from django.utils.translation import ugettext_lazy as _


twitter_publication_panel = [MultiFieldPanel([
    FieldPanel('twitter_enable_publish'),
    FieldPanel('twitter_consumer_secret'),
    FieldPanel('twitter_consumer_key'),
    FieldPanel('twitter_api_secret'),
    FieldPanel('twitter_api_key'),
    FieldPanel('twitter_owner'),
    FieldPanel('twitter_owner_id'),
], heading=_('Enable Twitter Publish'), classname='collapsible')]

twitter_block_panel = [
    MultiFieldPanel([
        StreamFieldPanel('twitter'),
    ], heading=_("Last tweets from"), classname="collapsible")
]