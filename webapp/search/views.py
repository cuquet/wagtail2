from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.search.models import Query
from ..base.models import BaseSiteSettings
from ..blog.models import EntryPage


def search(request):
    search_query = request.GET.get('query', None)
    site_settings = BaseSiteSettings.for_site(request.site)
    page_size = 10

    if hash(site_settings.num_results_page):
        page_size = site_settings.num_results_page

    # Search
    if search_query:
        if 'elasticsearch' in settings.WAGTAILSEARCH_BACKENDS['default']['BACKEND']:
            # In production, use ElasticSearch and a simplified search query, per
            # http://docs.wagtail.io/en/v1.12.1/topics/search/backends.html
            # like this:
            search_results = Page.objects.live().search(search_query)
        else:
            # If we aren't using ElasticSearch for the demo, fall back to native db search.
            # But native DB search can't search specific fields in our models on a `Page` query.
            # So for demo purposes ONLY, we hard-code in the model names we want to search.
            blog_results = EntryPage.objects.live().search(search_query)
            blog_page_ids = [p.page_ptr.id for p in blog_results]

            # page_ids = blog_page_ids
            search_results = Page.objects.live().filter(id__in=blog_page_ids)

        query = Query.get(search_query)

        # Record hit
        query.add_hit()

    else:
        search_results = Page.objects.none()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(search_results, page_size)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
