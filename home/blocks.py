from django.utils.functional import cached_property
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images import get_image_model
from wagtail.images.blocks import ImageChooserBlock
from wagtail_html_editor.blocks import EnhancedHTMLBlock


class IconTextItem(StructBlock):
    text = CharBlock(
        label="Текст",
        max_length=255,
    )
    icon = CharBlock(
        max_length=50,
        label="Иконка",
        help_text="Например: fa-bed, fa-wifi. https://fontawesome.com/search?q=cat&ic=free-collection",
    )

    class Meta:
        icon = "list-ul"


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock(
        required=True,
        label="Изображение",
    )
    caption = CharBlock(
        required=False,
        label="Подпись",
    )
    attribution = CharBlock(
        required=False,
        label="Автор",
    )

    @cached_property
    def preview_image(self):
        return get_image_model().objects.last()

    def get_preview_value(self):
        return {
            **self.meta.preview_value,
            "image": self.preview_image,
            "caption": self.preview_image.description,
        }

    class Meta:
        icon = "image"
        template = "blocks/captioned_image_block.html"
        preview_value = {"attribution": ""}
        label = "Изображение"
        description = "Изображение с подписью"


class HeadingBlock(StructBlock):
    heading_text = CharBlock(
        classname="title",
        required=True,
        label="Текст",
    )
    size = ChoiceBlock(
        choices=[
            ("", "Выберите заголовок"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
        label="Размер",
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"
        preview_value = {"heading_text": "Заголовок", "size": "h2"}
        label = "Заголовок"
        description = "Разные заголовки"


class ThemeSettingsBlock(StructBlock):
    theme = ChoiceBlock(
        choices=[
            ("default", "Default"),
            ("highlight", "Highlight"),
        ],
        required=False,
        default="default",
    )
    text_size = ChoiceBlock(
        choices=[
            ("default", "Default"),
            ("large", "Large"),
        ],
        required=False,
        default="default",
    )

    class Meta:
        icon = "cog"
        label_format = "Тема: {тема}, Размер: {размер}"


class BlockQuote(StructBlock):
    text = TextBlock(
        label="Текст",
    )
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")
    settings = ThemeSettingsBlock(collapsed=True)

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"
        label = "Цитата"


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        label="Параграф",
    )
    html_block = EnhancedHTMLBlock(
        label="Код HTML",
    )
    image_block = CaptionedImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        icon="media",
        template="blocks/embed_block.html",
        preview_template="base/preview/static_embed_block.html",
        label="Встраиваемое видео",
    )
