from django.template import Library
from django.urls import resolve
from django.template.loader import render_to_string
from django.template.defaultfilters import urlencode
from django_social_share.templatetags.social_share import _build_url
# from el_pagination.templatetags.el_pagination_tags import show_pages, paginate

from ..urls import get_entry_url, get_feeds_url
from ..models import Category, Tag
from ..utils import get_weight_fun
register = Library()


@register.inclusion_tag('blog/tags/entries_list.html', takes_context=True)
def recent_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-date')
    if limit:
        entries = entries[:limit]
    context['entries'] = entries
    return context


@register.inclusion_tag('blog/tags/entries_list.html', takes_context=True)
def popular_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-num_comments', '-date')
    if limit:
        entries = entries[:limit]
    context['entries'] = entries
    return context


@register.inclusion_tag('blog/tags/tags_list.html', takes_context=True)
def tags_list(context, limit=None, tags_qs=None):
    blog_page = context['blog_page']
    if tags_qs:
        tags = tags_qs.all()
    else:
        tags = Tag.objects.most_common(blog_page)
    if limit:
        tags = tags[:limit]
    context['tags'] = tags
    return context


@register.inclusion_tag('blog/tags/categories_table.html', takes_context=True)
def categories_table(context, categories_qs=None):
    blog_page = context['blog_page']
    if categories_qs:
        categories = categories_qs.all()
    else:
        categories = Category.objects.with_uses(blog_page).filter(parent=None)

    for category in categories:
        category.cat_entries = len(blog_page.get_entries().filter(entry_categories__category__slug=category.slug))

    context['categories'] = categories
    return context


@register.inclusion_tag('blog/tags/categories_list.html', takes_context=True)
def categories_list(context, categories_qs=None):
    blog_page = context['blog_page']
    if categories_qs:
        categories = categories_qs.all()
    else:
        categories = Category.objects.with_uses(blog_page).filter(parent=None)
    context['categories'] = categories
    return context


@register.inclusion_tag('blog/tags/archives_list.html', takes_context=True)
def archives_list(context):
    blog_page = context['blog_page']
    context['archives'] = blog_page.get_entries().datetimes('date', 'day', order='DESC')
    return context


@register.simple_tag(takes_context=True)
def entry_url(context, entry, blog_page):
    return get_entry_url(entry, blog_page.page_ptr, context['request'].site.root_page)


@register.simple_tag(takes_context=True)
def canonical_url(context, entry=None):
    if entry and resolve(context.request.path_info).url_name == 'wagtail_serve':
        return context.request.build_absolute_uri(entry_url(context, entry, entry.blog_page))
    return context.request.build_absolute_uri()


@register.simple_tag(takes_context=True)
def image_url(context, url):
    return context.request.build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def feeds_url(context, blog_page):
    return get_feeds_url(blog_page.page_ptr, context['request'].site.root_page)


@register.simple_tag(takes_context=True)
def show_comments(context):
    blog_page = context['blog_page']
    entry = context['self']
    if blog_page.display_comments and blog_page.disqus_shortname:
        ctx = {
            'disqus_shortname': blog_page.disqus_shortname,
            'disqus_identifier': entry.id
        }
        return render_to_string('blog/comments/disqus.html', context=ctx)
    return ""


# Avoid to import endless_pagination in installed_apps and in the templates
# register.tag('show_paginator', show_pages)
# register.tag('paginate', paginate)


@register.simple_tag(takes_context=True)
def post_to_linkendin_url(context, obj_or_url=None):
    request = context.get('request')
    if request:
        url = _build_url(request, obj_or_url)
        context['linkendin_url'] = 'https://www.linkedin.com/shareArticle?url={}'.format(urlencode(url))
    return context


@register.inclusion_tag('blog/tags/post_to_linkedin.html', takes_context=True)
def post_to_linkendin(context, obj_or_url=None, link_text='Post to Linkedin'):
    context = post_to_linkendin_url(context, obj_or_url)
    context['link_text'] = link_text
    return context
# https://github.com/feuervogel/django-taggit-templatetags/blob/master/taggit_templatetags/templatetags/taggit_extras.py


@register.inclusion_tag('blog/tags/tags_cloud.html', takes_context=True)
def tags_cloud(context):
    blog_page = context['blog_page']
    tags = Tag.objects.most_common(blog_page)

    counts = [tagitem.num_times for tagitem in tags]
    if counts:
        min_count, max_count = min(counts), max(counts)
        t__m_a_x = 10.0
        t__m_i_n = 1.0

        if blog_page.num_tags_size_in_cloud:
            t__m_a_x = blog_page.num_tags_size_in_cloud
        # TODO
        weight_fun = get_weight_fun(t__m_i_n, t__m_a_x, min_count, max_count)

        for tag in tags:
            tag.weight = int(weight_fun(tag.num_times))
    return {'blog_page': blog_page, 'request': context['request'], 'tags': tags}
    # else:
    #    return ''
