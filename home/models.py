from django.db import models
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import Collection, Page
from wagtailcache.cache import WagtailCacheMixin

from .blocks import BaseStreamBlock, IconTextItem


class HomePage(WagtailCacheMixin, Page):
    pass


# TODO: home page, header
#
@register_setting(icon="comment")
class GenericSettings(BaseGenericSetting):
    address_short = models.CharField(
        max_length=100,
        verbose_name="Адрес (короткий)",
        blank=False,
        null=False,
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес",
        blank=False,
        null=False,
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name="Email",
        blank=False,
        null=False,
    )
    social_vk = models.URLField(verbose_name="VK URL", blank=True)
    social_ok = models.URLField(verbose_name="OK URL", blank=True)
    social_rutube = models.URLField(verbose_name="Rutube URL", blank=True)
    social_yandex = models.URLField(verbose_name="Yandex URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("address"),
                FieldPanel("address_short"),
                FieldPanel("phone"),
                FieldPanel("email"),
                FieldPanel("social_vk"),
                FieldPanel("social_ok"),
                FieldPanel("social_rutube"),
                FieldPanel("social_yandex"),
            ],
            "Контакты",
        )
    ]

    class Meta:
        verbose_name = "Контакты"


class StandardPage(Page):
    introduction = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Титульное изображение",
    )
    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Содержимое",
        blank=True,
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]

    class Meta:
        verbose_name = "Страница"


class BaseObject(WagtailCacheMixin, Page):
    """Base abstract object."""

    introduction = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Титульное изображение",
    )
    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Содержимое",
        blank=True,
        use_json_field=True,
    )
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Коллекция изображений",
    )
    video_collection = StreamField(
        [
            (
                "videos",
                blocks.ListBlock(
                    blocks.RawHTMLBlock(),
                    label="Код видео",
                    collapsed=True,
                ),
            ),
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Коллекция видео",
    )
    features = StreamField(
        [("feature", IconTextItem())],
        blank=True,
        verbose_name="Особенности объекта",
        collapsed=True,
    )

    class Meta:
        abstract = True


class RoomPage(BaseObject):
    room_size = models.TextField(
        null=False,
        blank=False,
        verbose_name="Размер номера",
        help_text="Пример: 14-20м2",
    )
    adults = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Количество взрослых",
    )
    children = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name="Количество детей",
    )
    beds = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Количество спальных мест",
    )
    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("collection"),
        FieldPanel("video_collection"),
    ]

    room_panels = [
        FieldPanel("room_size"),
        FieldPanel("adults"),
        FieldPanel("children"),
        FieldPanel("beds"),
        FieldPanel("features"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Контент"),
            ObjectList(room_panels, heading="Детали номера"),
            ObjectList(Page.promote_panels, heading="Продвижение"),
            ObjectList(Page.settings_panels, heading="Настройки"),
        ]
    )

    class Meta:
        verbose_name = "Номер"


class GalleryPage(BaseObject):
    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("collection"),
        FieldPanel("video_collection"),
        FieldPanel("features"),
    ]

    class Meta:
        verbose_name = "Галерея"
