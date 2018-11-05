from django.utils.translation import ugettext_lazy as _
from wagtail.core.blocks import CharBlock, StructBlock


class TwitterBlock(StructBlock):
    twitter_box_username = CharBlock(required=True)
    twitter_box_widget_id = CharBlock(required=True)
    twitter_box_tweet_limit = CharBlock(required=True, max_length=2)

    class Meta:
        template = 'wagtail_block_twitter/blocks/block_twitter.html'
        icon = 'site'
        label = _('Twitter Widget')
        form_classname = 'struct-block'
