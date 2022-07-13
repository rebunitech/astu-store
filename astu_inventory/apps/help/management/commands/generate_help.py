from django.core.management.base import BaseCommand, CommandError
from django.urls import get_resolver, URLResolver

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)



class Command(BaseCommand):
    help = "Generate help index for every view"

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_pattern
        for url_pattern in url_patterns
