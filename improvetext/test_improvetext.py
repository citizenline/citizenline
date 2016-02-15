from django.test import TestCase

# Create your util here.
from django.contrib.sites.models import Site
from improvetext.models import Type


class PopulateTypesTestCase(TestCase):
    def setUp(self):
        # site = Site.objects.create(
        #     id=1,
        #     domain='www.example.com',
        #     name='www.example.com',
        # )
        site = Site.objects.get(id=1)

        Type.objects.create(
            id=1,
            site=site,
            name='Letter',
        )

    def test_populate_types(self):
        """
        Populate types
        :return:
        """
        first_type = Type.objects.get(id=1)
        self.assertEqual(first_type.name, 'Letter')
        #
        self.assertEqual(first_type.site.domain, 'example.com')
