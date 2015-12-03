# -*- coding: utf-8 -*-
import os

from django.core.management import call_command
from django.db.models import get_models
from django.test import TestCase
from django.utils.six import StringIO


class PrintModelsTest(TestCase):
    """ Test print_model """
    def test_command_output_model_names(self):
        """ Test print_model output all existing models """
        out = StringIO()
        with open(os.devnull, "w") as f:
            call_command('print_models', stdout=out, stderr=f)
        for model in get_models(include_auto_created=True):
            self.assertIn(model.__name__, out.getvalue())

    def test_command_output_total_number_of_objects_in_model(self):
        """ Test print_model output total number of objects per model """
        out = StringIO()
        with open(os.devnull, "w") as f:
            call_command('print_models', stdout=out, stderr=f)
        for model in get_models(include_auto_created=True):
            self.assertIn('Model name: %s, total number of '
                          'objects: %s' % (model.__name__,
                                           model._default_manager.count()),
                          out.getvalue())
