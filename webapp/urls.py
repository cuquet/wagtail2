from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import set_language, JavaScriptCatalog
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls

from webapp.search import views as search_views
from .api import api_router
from .blog import urls as blog_urls


js_info_dict = {
    'packages': ('webapp',)
}

urlpatterns = [
    url('^sitemap\.xml$', sitemap),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^api/v2/', api_router.urls),
]

urlpatterns += i18n_patterns(
    url(r'^i18n/$', set_language, name='set_language'),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'', include(blog_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView
    from django.views.generic.base import RedirectView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(
            r'^favicon\.ico$', RedirectView.as_view(
                url=settings.STATIC_URL + 'images/favicon/favicon.ico'
                )
            )
    ]

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        url(r'^test404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^test500/$', TemplateView.as_view(template_name='500.html')),
        url(r'^components/$', TemplateView.as_view(template_name='components.html')),
    ]

