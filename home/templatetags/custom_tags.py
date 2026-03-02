from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django import template
from django.core.cache import cache
from wagtail.images import get_image_model

from home.models import GenericSettings

register = template.Library()


@register.simple_tag
def booking_link():
    today = datetime.today().date()
    date_format = "%d.%m.%Y"
    value = cache.get(today.strftime(date_format))
    if value:
        return value

    settings = GenericSettings.load()
    url = settings.book_link
    if not url:
        return ""
    parsed_url = urlparse(settings.book_link)
    params = parse_qs(parsed_url.query)
    begin = datetime.strptime(params["search_form[begin]"][0], "%d.%m.%Y").date()
    if today > begin:
        end = today + timedelta(days=3)
        params["search_form[begin]"] = [today.strftime("%d.%m.%Y")]
        params["search_form[end]"] = [end.strftime("%d.%m.%Y")]
        new_query = urlencode(params, doseq=True)

        url = urlunparse(parsed_url._replace(query=new_query))

    cache.set(today.strftime(date_format), url, 60 * 60 * 24)
    return url


@register.simple_tag
def collection_images(collection):
    """
    Returns a queryset of images from a Wagtail Collection.
    Usage:
        {% collection_images page.featured_photos as photos %}
        {% for photo in photos %}
            <img src="{{ photo.file.url }}" />
        {% endfor %}
    """
    if not collection:
        return []

    return get_image_model().objects.filter(collection=collection)


@register.simple_tag
def collection_images_recursive(collection):
    """
    Returns images from collection AND all its sub-collections.
    """
    if not collection:
        return []
    collections = collection.get_descendants(inclusive=True)
    return get_image_model().objects.filter(collection__in=collections)


@register.filter
def get_item(collection, index):
    try:
        return collection[index]
    except IndexError:
        return None


@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ""


@register.filter
def first_half(value):
    """Return first half of collection"""
    try:
        mid = len(value) // 2
        return value[:mid]
    except (TypeError, AttributeError):
        return value


@register.filter
def second_half(value):
    """Return second half of collection"""
    try:
        mid = len(value) // 2
        return value[mid:]
    except (TypeError, AttributeError):
        return []
