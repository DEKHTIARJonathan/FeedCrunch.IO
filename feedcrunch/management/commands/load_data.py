#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import csv

from django.core.management.base import BaseCommand

from feedcrunch.models import *
from application.settings import *


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)

    for row in csv_reader:
        yield [str(cell) for cell in row]


class Command(BaseCommand):
    help = 'Load Data from continents.csv and countries.csv'

    def handle(self, *args, **options):

        ## Load Continents to DATABASE

        print("Saving Continents ...")
        with open(os.path.join(BASE_DIR, 'feedcrunch/data/continents.csv'), 'rb') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                cntnt = Continent(code=row[0], name=row[1])
                cntnt.save()
        print("Continents Saved !")

        ## Load Countries to DATABASE

        print("Saving Countries ...")
        with open(os.path.join(BASE_DIR, 'feedcrunch/data/countries.csv'), 'rb') as f:
            reader = unicode_csv_reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                cntry = Country(continent=Continent.objects.get(name=row[2]), code=row[1], name=row[0])
                cntry.save()
        print("Countries Saved !")
