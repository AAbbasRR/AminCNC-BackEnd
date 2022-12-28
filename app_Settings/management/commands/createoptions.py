from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from app_Settings.models import SiteOptions

import csv
import codecs


class Command(BaseCommand):
    help = 'Initiate DB with options csv file'

    def handle(self, *args, **options):
        options_path = 'options.csv'
        with open(options_path, 'rb') as options_file:
            option_reader = csv.reader(codecs.iterdecode(options_file, 'utf-8'))
            option_header = next(option_reader)
            for row in option_reader:
                _object_dict = {key: value for key, value in zip(option_header, row)}
                try:
                    SiteOptions.objects.create(**_object_dict)
                except IntegrityError:
                    pass
