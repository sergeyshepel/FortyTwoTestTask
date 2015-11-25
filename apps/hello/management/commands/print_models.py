from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    help = 'Print all objects in models'

    def handle(self, *args, **options):
        for model in get_models(include_auto_created=True):
            line_to_print = 'Model name: %s, total number of ' \
                            'objects: %s' % (model.__name__,
                                             model._default_manager.count())
            self.stdout.write(line_to_print)
            self.stderr.write('error: ' + line_to_print)
