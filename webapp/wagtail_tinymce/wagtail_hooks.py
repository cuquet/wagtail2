# Copyright (c) 2016, Isotoma Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Isotoma Limited nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ISOTOMA LIMITED BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import json

from django import __version__ as DJANGO_VERSION
from django.utils.html import format_html, format_html_join, escape
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils import translation
from django.utils.safestring import mark_safe
from django.conf import settings
from django.urls import reverse

from wagtail.admin.templatetags.wagtailadmin_tags import hook_output
from wagtail.core import hooks
from wagtail.admin.rich_text.converters.editor_html import WhitelistRule
from wagtail.core.whitelist import allow_without_attributes, attribute_rule


def to_js_primitive(string):
    return mark_safe(escape(string))


@hooks.register('insert_editor_css')
def insert_editor_css():
    css_files = [
        'wagtail_tinymce/css/icons.css'
    ]
    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}">',
        ((settings.STATIC_URL, filename) for filename in css_files),
    )
    return css_includes + hook_output('insert_tinymce_css')


@hooks.register('insert_editor_js')
def insert_editor_js():
    preload = format_html(
        """
        <script>
        (function() {{
            "use strict";
            window.tinymce = window.tinymce || {{}};
            window.tinymce.base = window.tinymce.baseURL = "{}";
            window.tinymce.suffix = "";
        }}());
        </script>
        """,
        mark_safe(escape(static('wagtail_tinymce/js/vendor/tinymce/'))),
    )
    js_files = [
        'wagtail_tinymce/js/vendor/tinymce/tinymce.min.js',
        'wagtail_tinymce/js/vendor/tinymce/jquery.tinymce.min.js',
        'wagtail_tinymce/js/tinymce-editor.js',
    ]
    js_includes = format_html_join(
        '\n',
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return preload + js_includes + hook_output('insert_tinymce_js')


@hooks.register('insert_tinymce_js')
def images_richtexteditor_js():
    return format_html(
        """
        <script>
            registerMCEPlugin("wagtailimage", "{}", "{}");
            window.chooserUrls.imageChooserSelectFormat = "{}";
        </script>
        """,
        to_js_primitive(static('wagtail_tinymce/js/tinymce-plugins/wagtailimage.js')),
        to_js_primitive(translation.to_locale(translation.get_language())),
        to_js_primitive(reverse('wagtailimages:chooser_select_format', args=['00000000']))
    )


@hooks.register('insert_tinymce_js')
def embeds_richtexteditor_js():
    return format_html(
        """
        <script>
            registerMCEPlugin("wagtailembeds", "{}", "{}");
        </script>
        """,
        to_js_primitive(static('wagtail_tinymce/js/tinymce-plugins/wagtailembeds.js')),
        to_js_primitive(translation.to_locale(translation.get_language())),
    )


@hooks.register('insert_tinymce_js')
def links_richtexteditor_js():
    return format_html(
        """
        <script>
            registerMCEPlugin("wagtaillink", "{}", "{}");
        </script>
        """,
        to_js_primitive(static('wagtail_tinymce/js/tinymce-plugins/wagtaillink.js')),
        to_js_primitive(translation.to_locale(translation.get_language())),
    )


@hooks.register('insert_tinymce_js')
def docs_richtexteditor_js():
    return format_html(
        """
        <script>
            registerMCEPlugin("wagtaildoclink", "{}", "{}");
        </script>
        """,
        to_js_primitive(static('wagtail_tinymce/js/tinymce-plugins/wagtaildoclink.js')),
        to_js_primitive(translation.to_locale(translation.get_language())),
    )


@hooks.register('register_rich_text_features')
def boostraptypography_feature(features):
    features.register_converter_rule('editorhtml', 'boostraptypography', [
        WhitelistRule('div', attribute_rule({'class': True})),
        WhitelistRule('p', attribute_rule({'class': True})),
        WhitelistRule('small', attribute_rule({'class': True})),
        WhitelistRule('ul', attribute_rule({'class': True})),
        WhitelistRule('li', attribute_rule({'class': True})),
        WhitelistRule('dl', attribute_rule({'class': True})),
        WhitelistRule('dt', attribute_rule({'class': True})),
        WhitelistRule('dd', attribute_rule({'class': True})),
        WhitelistRule('span', attribute_rule({'class': True})),

    ])

    features.default_features.append('boostraptypography')

