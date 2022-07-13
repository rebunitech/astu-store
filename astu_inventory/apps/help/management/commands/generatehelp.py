import itertools

from django.core.management.base import BaseCommand
from django.urls import URLResolver, get_resolver

from astu_inventory.apps.help.models import Help


class Command(BaseCommand):
    help = "Generate help index for every view"

    def get_url_patterns(self, url_resolver):
        for url_pattern in url_resolver.url_patterns:
            if isinstance(url_pattern, URLResolver):
                yield from self.get_url_patterns(url_pattern)
            else:
                if url_pattern.name is None:
                    continue
                yield url_pattern.name

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        for url_pattern in url_patterns:
            if isinstance(url_pattern, URLResolver):
                app_name = getattr(url_pattern, "app_name")
                if app_name is None:
                    continue
                Help.objects.bulk_create(
                    [
                        Help(app_name=help_app_name, view_name=help_view_name)
                        for help_app_name, help_view_name in itertools.zip_longest(
                            (app_name,), self.get_url_patterns(url_pattern), fillvalue=app_name
                        )
                    ],
                    ignore_conflicts=True,
                )
        print("Help index generated successfully!")
