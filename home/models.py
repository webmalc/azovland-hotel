from django.db import models
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.documents.models import Document
from wagtail.fields import StreamField
from wagtail.models import Collection, Page
from wagtailcache.cache import WagtailCacheMixin

from .blocks import BaseStreamBlock, IconTextItem, ReviewBlock

# TODO:   azovland: 9,10 template, header + video,menu, stats (happy customers, etc),
# rooms: tile, descrit, size 14-20m2, adults + childer, amenities, beds, calc -> az, photo, photo title
# objects: title, descrip, photo, video, amenities, photo title (9 template blog)
# contats - about: just page, yandex.map
#


class HomePage(WagtailCacheMixin, Page):
    header_1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Заголовок 1",
    )
    text_1 = models.TextField(
        blank=True,
        verbose_name="Текст 1",
    )
    header_2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Заголовок 2",
    )
    text_2 = models.TextField(
        blank=True,
        verbose_name="Текст 2",
    )

    # videos
    bg_video_size_l = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="+",
        verbose_name="Фоновое видео (большое)",
    )
    bg_video_size_m = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Фоновое видео (среднее)",
    )
    bg_video_size_s = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Фоновое видео (малое)",
    )

    # features
    stats = StreamField(
        [("feature", IconTextItem(label="Статистика"))],
        blank=True,
        verbose_name="Статистика отеля",
        collapsed=True,
    )
    activities = StreamField(
        [("feature", IconTextItem(label="Активность"))],
        blank=True,
        verbose_name="Активности отеля",
        collapsed=True,
    )
    facilities = StreamField(
        [("feature", IconTextItem(label="Услуга"))],
        blank=True,
        verbose_name="Услуги/инфраструктура отеля",
        collapsed=True,
    )

    # pages
    featured_section_1_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Заголовок раздела 1",
    )
    featured_section_1 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Раздел 1",
    )
    featured_section_2_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Заголовок раздела 2",
    )
    featured_section_2 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Раздел 2",
    )
    featured_section_3_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Заголовок раздела 3",
    )
    featured_section_3 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Раздел 3",
    )

    # other
    reviews = StreamField(
        [("feature", ReviewBlock(label="Отзыв"))],
        blank=True,
        verbose_name="Отзывы клиентов",
        collapsed=True,
    )
    featured_photos_1 = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Избранные изображения 1",
    )
    featured_photos_2 = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Избранные изображения 2",
    )
    featured_photos_3 = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Избранные изображения 3",
    )

    # panels
    content_panels = Page.content_panels + [
        FieldPanel("bg_video_size_l"),
        FieldPanel("bg_video_size_m"),
        FieldPanel("bg_video_size_s"),
    ]
    features_panels = [
        FieldPanel("stats"),
        FieldPanel("activities"),
        FieldPanel("facilities"),
    ]
    other_panels = [
        FieldPanel("reviews"),
        FieldPanel("featured_photos_1"),
        FieldPanel("featured_photos_2"),
        FieldPanel("featured_photos_3"),
    ]
    sections_panels = [
        FieldPanel("featured_section_1_title"),
        FieldPanel("featured_section_1"),
        FieldPanel("featured_section_2_title"),
        FieldPanel("featured_section_2"),
        FieldPanel("featured_section_3_title"),
        FieldPanel("featured_section_3"),
    ]
    text_panels = [
        FieldPanel("header_1"),
        FieldPanel("text_1"),
        FieldPanel("header_2"),
        FieldPanel("text_2"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Контент"),
            ObjectList(features_panels, heading="Особенности отеля"),
            ObjectList(sections_panels, heading="Разделы"),
            ObjectList(text_panels, heading="Текст"),
            ObjectList(other_panels, heading="Другое"),
            ObjectList(Page.promote_panels, heading="Продвижение"),
            ObjectList(Page.settings_panels, heading="Настройки"),
        ]
    )


@register_setting(icon="comment")
class GenericSettings(BaseGenericSetting):
    book_link = models.URLField(
        verbose_name="Ссылка на бронирование",
        blank=True,
    )
    book_link_text = models.CharField(
        verbose_name="Текст ссылки на бронирование",
        blank=True,
    )
    address_short = models.CharField(
        max_length=100,
        verbose_name="Адрес (короткий)",
        blank=False,
        null=False,
    )
    address = models.TextField(
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
                FieldPanel("book_link"),
                FieldPanel("book_link_text"),
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
        [("feature", IconTextItem(label="Особенность"))],
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
