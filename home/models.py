from wagtail.models import Page
from wagtailcache.cache import WagtailCacheMixin


class HomePage(WagtailCacheMixin, Page):
    pass
