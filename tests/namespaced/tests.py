from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpRequest
from django.test import TestCase
from django.utils import simplejson as json


class NamespacedViewsTestCase(TestCase):
    urls = 'namespaced.api.urls'

    def test_urls(self):
        from namespaced.api.urls import api
        patterns = api.urls
        self.assertEqual(len(patterns), 3)
        self.assertEqual(sorted([pattern.name for pattern in patterns if hasattr(pattern, 'name')]), ['api_v1_top_level'])
        self.assertEqual([[pattern.name for pattern in include.url_patterns if hasattr(pattern, 'name')] for include in patterns if hasattr(include, 'reverse_dict')], [['api_dispatch_list', 'api_get_schema', 'api_get_multiple', 'api_dispatch_detail'], ['api_dispatch_list', 'api_get_schema', 'api_get_multiple', 'api_dispatch_detail']])

        self.assertRaises(NoReverseMatch, reverse, 'api_v1_top_level')
        self.assertRaises(NoReverseMatch, reverse, 'special:api_v1_top_level')
        self.assertEquals(reverse('special:api_v1_top_level', kwargs={'api_name': 'v1'}), '/api/v1/')
        self.assertEquals(reverse('special:api_dispatch_list', kwargs={'api_name': 'v1', 'resource_name': 'notes'}), '/api/v1/notes/')
