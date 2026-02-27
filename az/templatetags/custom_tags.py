from django import template
from wagtail.images import get_image_model

register = template.Library()


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
