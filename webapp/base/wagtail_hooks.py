from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html_join
from django.conf import settings

from wagtail.core import hooks


@hooks.register('insert_global_admin_css')
def global_admin_css():
    css_files = [
        'css/jquery.fonticonpicker.min.css',
        'css/jquery.fonticonpicker.grey.min.css',
        'css/pe-icon-7-stroke.css',
        'local/fontello/css/fontawesome.css'
    ]
    css_includes = format_html_join('\n', '<link rel="stylesheet" href="{0}{1}"/>',
                                    ((settings.STATIC_URL, filename) for filename in css_files))
    # return format_html('<link rel="stylesheet" href="{}">', static('my/wagtail/theme.css'))
    return css_includes


@hooks.register('insert_global_admin_js')
def global_admin_js():
    js_files = [
        'js/jquery.fonticonpicker.min.js',
        'js/jquery.wagtail.iconpicker.js',
    ]
    js_includes = format_html_join('\n', '<script type="text/javascript" src="{0}{1}" ></script>',
                                   ((settings.STATIC_URL, filename) for filename in js_files))
    #return format_html('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r74/three.js"></script>',)
    return js_includes
