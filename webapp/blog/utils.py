from six import string_types
from importlib import import_module
from django.urls import reverse


def import_model(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def get_image_model_path():
    from django.conf import settings
    return getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'wagtailimages.Image')


def get_weight_fun(t_min, t_max, f_min, f_max):
    def weight_fun(f_i, t_min=t_min, t_max=t_max, f_min=f_min, f_max=f_max):
        # Prevent a division by zero here, found to occur under some
        # pathological but nevertheless actually occurring circumstances.
        if f_max == f_min:
            mult_fac = 1.0
        else:
            mult_fac = float(t_max - t_min) / float(f_max - f_min)

        return t_max - (f_max - f_i) * mult_fac

    return weight_fun


def strip_prefix_and_ending_slash(path):
    """
    If blog and wagtail are registered with a prefix, it needs to be removed
    so the 'entry_page_serve_slug' or 'blog_page_feed_slug' resolutions can work.
    Ex, here with a dynamic (i18n_patterns()) + a static prefix :
    urlpatterns += i18n_patterns(
        url(r'^blah/', include('blog.urls')),
        url(r'^blah/', include(wagtail_urls)),
    )
    The prefix is simply the root where Wagtail page are served.
    https://github.com/torchbox/wagtail/blob/stable/1.8.x/wagtail/wagtailcore/urls.py#L36
    """
    return path.replace(reverse('wagtail_serve', args=[""]), '', 1).rstrip("/")
