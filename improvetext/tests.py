from django.test import TestCase

# Create your tests here.

from improvetext.models import Type


class PopulateTypesTests(TestCase):

    def test_populate_types(self):
        """
        Populate types
        :return:
        """
