try:
    from wagtail import __version__ as WAGTAIL_VERSION
except ImportError:  # fallback for Wagtail <2.0
    from wagtail.wagtailcore import __version__ as WAGTAIL_VERSION
