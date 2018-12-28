from django import template
from django.conf import settings

from wagtail.core.models import Page

from webapp.base.models import FooterText
from webapp.blog.models import BlogPage, Category

register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/


# settings value
@register.simple_tag
def get_google_maps_key():
    return getattr(settings, 'GOOGLE_MAPS_KEY', "")


@register.simple_tag(takes_context=True)
def get_site_root(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    return context['request'].site.root_page


def has_menu_children(page):
    # This is used by the top_menu property
    # get_children is a Treebeard API thing
    # https://tabo.pe/projects/django-treebeard/docs/4.0.1/api.html
    return page.get_children().live().in_menu().exists()


def has_children(page):
    # Generically allow index pages to list their children
    return page.get_children().live().exists()


def is_active(page, current_page):
    # To give us active state on main navigation
    return current_page.url_path.startswith(page.url_path) if current_page else False


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the Foundation menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None, show_search=True):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.url_path.startswith(menuitem.url_path)
                           if calling_page else False)
    return {
        'show_search': show_search,
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent, calling_page=None):
    parent.type = parent.specific_class.__name__
    if parent.type == 'BlogPage':
        blog_page = BlogPage.objects.live().filter(pk=parent.pk)[0]
        menuitems_children = Category.objects.with_uses(blog_page).filter(parent=None)
        for menuitem in menuitems_children:
            menuitem.title = menuitem.name
            menuitem.url = parent.url + blog_page.reverse_subpage('entries_by_category', args=(menuitem.slug, ))
    else:
        menuitems_children = parent.get_children()
        menuitems_children = menuitems_children.live().in_menu()
        for menuitem in menuitems_children:
            menuitem.has_dropdown = has_menu_children(menuitem)
            # We don't directly check if calling_page is None since the template
            # engine can pass an empty string to calling_page
            # if the variable passed as calling_page does not exist.
            menuitem.active = (calling_page.url_path.startswith(menuitem.url_path)
                               if calling_page else False)
            menuitem.children = menuitem.get_children().live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=1)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }


@register.inclusion_tag('blocks/block_footer_text.html', takes_context=True)
def get_footer_text(context):
    footer_text = ""
    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().rawhtml

    return {
        'footer_text': footer_text,
    }
