from django.conf import settings
from django.utils.html import format_html_join

from wagtail.core import hooks


@hooks.register('insert_global_admin_css')
def global_admin_css():
    css_files = [
        'css/jquery.fonticonpicker.min.css',
        'css/jquery.fonticonpicker.grey.min.css',
        'css/icomoon.css',
        'css/fontello.css'
    ]
    css_includes = format_html_join('\n', '<link rel="stylesheet" href="{0}{1}"/>',
                                    ((settings.STATIC_URL, filename) for filename in css_files))
    return css_includes


@hooks.register('insert_global_admin_js')
def global_admin_js():
    js_files = [
        'js/jquery.fonticonpicker.min.js',
        # 'js/jquery.wagtail.iconpicker.js',
    ]
    js_includes = format_html_join('\n', '<script type="text/javascript" src="{0}{1}" ></script>',
                                   ((settings.STATIC_URL, filename) for filename in js_files))
    return js_includes
