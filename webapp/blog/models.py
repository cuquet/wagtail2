from pkg_resources import parse_version

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import six

from wagtail.core.models import Page, PageBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase, Tag as TaggitTag
from modelcluster.fields import ParentalKey

from colorful.fields import RGBColorField

from webapp.base.abstracts import BaseMinimalPageAbstract
from webapp.wagtail_block_twitter.abstracts import MyTwitterPublishAbstract
from webapp.wagtail_block_twitter.panels import twitter_publication_panel


from .abstracts import EntryAbstract
from .utils import import_model
from .routes import BlogRoutes
from .managers import TagManager, CategoryManager, BlogManager

Entry = import_model(getattr(settings, 'BLOG_ENTRY_MODEL', EntryAbstract))


class BlogPage(BlogRoutes, MyTwitterPublishAbstract, BaseMinimalPageAbstract):

    main_color = RGBColorField(_('Blog Main Color'), default="#4D6AE0")

    display_comments = models.BooleanField(default=False, verbose_name=_('Display comments'))
    display_categories = models.BooleanField(default=True, verbose_name=_('Display categories'))
    display_tags = models.BooleanField(default=True, verbose_name=_('Display tags'))
    display_popular_entries = models.BooleanField(default=True, verbose_name=_('Display popular entries'))
    display_last_entries = models.BooleanField(default=True, verbose_name=_('Display last entries'))
    display_archive = models.BooleanField(default=True, verbose_name=_('Display archive'))

    disqus_api_secret = models.TextField(blank=True)
    disqus_shortname = models.CharField(max_length=128, blank=True)

    num_entries_page = models.IntegerField(default=5, verbose_name=_('Entries per page'))
    num_last_entries = models.IntegerField(default=3, verbose_name=_('Last entries limit'))
    num_popular_entries = models.IntegerField(default=3, verbose_name=_('Popular entries limit'))
    num_tags_entry_header = models.IntegerField(default=5, verbose_name=_('Tags limit entry header'))
    num_tags_size_in_cloud = models.IntegerField(default=8, verbose_name=_('Tags sizes in tag cloud'))

    short_feed_description = models.BooleanField(default=True, verbose_name=_('Use short description in feeds'))

    extra = BlogManager()

    content_panels = BaseMinimalPageAbstract.content_panels + [
        FieldPanel('main_color')
    ]
    settings_panels = BaseMinimalPageAbstract.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel('display_categories'),
                FieldPanel('display_tags'),
                FieldPanel('display_popular_entries'),
                FieldPanel('display_last_entries'),
                FieldPanel('display_archive'),
            ],
            heading=_("Widgets")
        ),
        MultiFieldPanel(
            [
                FieldPanel('num_entries_page'),
                FieldPanel('num_last_entries'),
                FieldPanel('num_popular_entries'),
                FieldPanel('num_tags_entry_header'),
                FieldPanel('num_tags_size_in_cloud'),

            ],
            heading=_("Parameters"), classname="collapsible"
        ),
        MultiFieldPanel(
            [
                FieldPanel('display_comments'),
                FieldPanel('disqus_api_secret'),
                FieldPanel('disqus_shortname'),
            ],
            heading=_("Comments")
        ),
        MultiFieldPanel(
            [
                FieldPanel('short_feed_description'),
            ],
            heading=_("Feeds")
        ),
    ] + twitter_publication_panel
    subpage_types = ['blog.EntryPage']

    def get_entries(self):
        return EntryPage.objects.descendant_of(self).live().order_by('-date').select_related('owner')

    def get_context(self, request, *args, **kwargs):
        # context = super(BlogPage, self).get_context(request, *args, **kwargs)
        # context['entries'] = self.entries
        # context['blog_page'] = self
        # context['search_type'] = getattr(self, 'search_type', "")
        # context['search_term'] = getattr(self, 'search_term', "")

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(self.entries, self.num_entries_page)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        # Update template context
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['entries'] = entries
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")

        return context

    @property
    def last_url_part(self):
        """
        Get the BlogPage url without the domain
        """
        return self.get_url_parts()[-1]

    class Meta:
        verbose_name = _('Blog')


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name=_('Category name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_('Parent category'),
        on_delete=models.SET_NULL
    )
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_('Parent category cannot be self.'))
            if parent.parent and parent.parent == self:
                raise ValidationError(_('Cannot have circular Parents.'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class CategoryEntryPage(models.Model):
    category = models.ForeignKey(Category, related_name="+", verbose_name=_('Category'), on_delete=models.CASCADE)
    page = ParentalKey('EntryPage', related_name='entry_categories')
    panels = [
        FieldPanel('category')
    ]

    def __str__(self):
        return str(self.category)


class TagEntryPage(TaggedItemBase):
    content_object = ParentalKey('EntryPage', related_name='entry_tags')


@register_snippet
class Tag(TaggitTag):
    objects = TagManager()

    class Meta:
        proxy = True


class EntryPageRelated(models.Model):
    entrypage_from = ParentalKey('EntryPage', verbose_name=_("Entry"), related_name='related_entrypage_from')
    entrypage_to = ParentalKey('EntryPage', verbose_name=_("Entry"), related_name='related_entrypage_to')

    def __str__(self):
        return str(self.entrypage_to)


def _add_owner_panel():
    """
    Since Wagtail 1.11 EntryPage owner is set as `editable` it can be added to EntryPage
    `settings_panels` if blog is using a version greater or equal than 1.11.

    See:
    https://github.com/wagtail/wagtail/pull/3581
    """
    return [FieldPanel('owner')]


class EntryPage(six.with_metaclass(PageBase, Entry, Page)):
    # Search
    search_fields = EntryAbstract.search_fields

    # Panels
    content_panels = EntryAbstract.content_panels

    promote_panels = EntryAbstract.promote_panels

    settings_panels = EntryAbstract.settings_panels + _add_owner_panel()

    # Parent and child settings
    parent_page_types = ['blog.BlogPage']
    subpage_types = []

    @property
    def blog_page(self):
        return self.get_parent().specific

    @property
    def related(self):
        return [related.entrypage_to for related in self.related_entrypage_from.all()]

    @property
    def has_related(self):
        return self.related_entrypage_from.count() > 0

    def get_context(self, request, *args, **kwargs):
        context = super(EntryPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
