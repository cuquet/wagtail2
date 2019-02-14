from django import forms
from django.utils.translation import get_language, ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings

from wagtail.admin.edit_handlers import BaseFormEditHandler, FieldPanel
from wagtail.core.blocks import BooleanBlock, CharBlock, ChoiceBlock, \
    FieldBlock, RawHTMLBlock, RichTextBlock, StreamBlock, StructBlock, \
    TextBlock, EmailBlock, IntegerBlock, FloatBlock, DecimalBlock, \
    RegexBlock, URLBlock, DateBlock, DateTimeBlock, TimeBlock, BlockQuoteBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock

CARD_CHOICES = (
    ('card-avatar', _('Avatar centered image')),
    ('', _('Plain')),
    ('card-background', _('Background')),
)

SIZE_CHOICES = (
    ('parallax-small', _("Small")),
    ('parallax-medium', _("Medium")),
    ('parallax-large', _("Large")),
)

FILTER_CHOICES = (
    ('filter filter-black', "filter-black"),
    ('filter filter-white', "filter-white"),
    ('filter filter-blue', "filter-blue"),
    ('filter filter-azure', "filter-azure"),
    ('filter filter-green', "filter-green"),
    ('filter filter-orange', "filter-orange"),
    ('filter filter-red', "filter-red"),
    ('filter filter-white', "filter-white"),
    ('', "No filter"),
)

IMG_CLASS_CHOICES = (
    ('rounded', "Rounded Corner"),
    ('rounded-circle', "Circle"),
    ('img-thumbnail', "Thumbnail"),
    ('img-fluid', "Responsive"),
    (' ', "No Shape"),
)
IMG_ALIGN_CHOICES = (
    ('float-left', 'Wrap left'),
    ('float-right', 'Wrap right'),
    ('mx-auto d-block', 'Mid width'),
)


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=False)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ],
        help_text=_('Custom StructBlock that allows the user to select h2 - h4 sizes for headers'),
        blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/block_heading.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        help_text=_('Custom StructBlock that allows the user to attribute a quote to the author'),
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "openquote"
        template = "blocks/block_quote.html"


class BaseImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    size = CharBlock(label=_('Image resize'), required=False,
                     help_text=_('It must be defined in wagtail picture redimension tag: width-640, height-480, '
                                 'fill-200x200-c100 or original (which is the default option)'))
    alignment = ChoiceBlock(choices=IMG_ALIGN_CHOICES, default=" ")
    shape = ChoiceBlock(choices=IMG_CLASS_CHOICES, default=" ")

    class Meta:
        icon = 'image'
        template = "blocks/block_image.html"


class BaseParallaxContentBlock(StructBlock):
    parallax_head=CharBlock(label=_("Head"), required=False, blank=True, classname="title",
                                help_text=_("You can split the title using '|'. It will add small .subtitle class."))
    parallax_text=RichTextBlock(label=_("Text"), required=False, null=True, blank=True)
    parallax_pro=CharBlock(label="Pro", required=False, null=True, blank=True)

    @property
    def media(self):
        return forms.Media(
            # css={'all': ['css/nnnn.css']},
        )

    class Meta:
        template = 'blocks/block_parallax_content.html'
        label = _('The Parallax content')
        form_classname = 'struct-block'
        # form_template = ''
        abstract = True


class BaseParallaxBlock(StructBlock):
    parallax_image = ImageChooserBlock()
    parallax_size = ChoiceBlock(choices=SIZE_CHOICES, default="parallax-large", help_text=_('Parallax size'))
    parallax_filter = ChoiceBlock(choices=FILTER_CHOICES, default="filter-black", help_text=_('Filter effect'))
    display_btndropdown = BooleanBlock(default=False, required=False, help_text=_('Display dropdown button'))
    parallax_content = BaseParallaxContentBlock()

    class Meta:
        template = 'blocks/block_parallax.html'
        form_template = 'edit_handlers/parallax_panel.html'
        form_classname = 'struct-block'
        icon = 'image'
        label = _('Parallax Block')
        abstract = True


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    intro = RichTextBlock(icon="pilcrow")
    paragraph_block = RichTextBlock(
        icon="form",
        template="blocks/block_paragraph.html"
    )
    aligned_image = BaseImageBlock(label=_('Aligned image'), icon="image")
    aligned_html = RawHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")
    block_quote = BlockQuote()
    block_parallax = BaseParallaxBlock()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="placeholder",
        template="blocks/block_embed.html")


class IconPanel(FieldPanel):
    TEMPLATE_VAR = 'iconfield_panel'

    def __init__(self, field_name, *args, **kwargs ):
        self.field_name = field_name
        widget = kwargs.pop('widget', None)
        if widget is not None:
            self.widget = widget
        super(IconPanel, self).__init__(self.field_name, *args, **kwargs)

    object_template = "edit_handlers/iconfield_panel.html"

    def render_as_object(self):
        return mark_safe(render_to_string(self.object_template, {
            'self': self,
            self.TEMPLATE_VAR: self,
            'field': self.bound_field,
        }))

    field_template = "edit_handlers/iconfield_panel.html"

    def render_as_field(self):
        return mark_safe(render_to_string(self.field_template, {
            'field': self.bound_field,
            'field_type': self.field_type(),
        }))
