from os.path import dirname, join, realpath
import time

from flask import request
from jinja2 import Environment, FileSystemLoader
from nose.plugins.attrib import attr

from briefscaster import app
from briefscaster import briefcast

# Backward compatible unittest
try:
    import unittest
    # skip was added in 2.7/3.1
    assert unittest.skip
except AttributeError:
    import unittest2 as unittest

HERE = dirname(__file__)
BRIEFCASTS = join(HERE, 'briefcasts')

env = Environment(loader=FileSystemLoader(join(HERE, 'expected')))


class TestBriefcast(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_will_provide_rss(self):
        items = briefcast.find_briefs(HERE)

        with app.test_request_context('/'):
            url_root = request.url_root

            rss = briefcast.create_feed(items, url_root)

            expected = env.get_template('example1.rss').render(
                src=realpath(join(HERE, '..', '../')),
                here=HERE,
                pub_date=time.strftime(briefcast.GMT_FORMAT, time.gmtime()),
            )

            self.assertEqual(rss, expected)

    def test_build_cache(self):
        items = briefcast.find_briefs(HERE)

        url_root = 'http://127.0.0.1:5000/'

        cache = briefcast.create_briefs_cache(items, url_root)

        key1, item1 = cache.items()[0]

        expected_hash = 'd27249fce1889f04b3471633826f043de0bafd2b'

        self.assertDictEqual({
            'bs_filename': '%s/briefcasts/example1/example1.bs' % HERE, 
            'filename': '%s/briefcasts/example1/example1.brieflist' % HERE,
            'description': 'Output from example1.bs',
            'title': 'example1.brieflist',
            'url': '%sbrieflist/%s' % (url_root, expected_hash,),
            'length': 27980, 'guid': '%s' % expected_hash,
            'pub_date': item1['pub_date']},
            item1)

    def test_find_briefs(self):
        briefs = [i for i in briefcast.find_briefs(HERE)]

        item1 = briefs[0]

        self.assertEquals('%s/briefcasts/example1/example1.bs' % HERE,
            item1)

    def test_serves_briefcase(self):
        response = self.client.get('/')

        self.assertIn(
            '<title>Briefs caster server on http://localhost/</title>',
            response.data)

    def test_serves_briefs(self):
        items = briefcast.find_briefs(HERE)

        with app.test_request_context('/'):
            url_root = request.url_root

            rss = briefcast.create_feed(items, url_root)
            briefs_cache = briefcast.get_briefs_cache()

            key = briefs_cache.keys()[0]

            response = self.client.get('/brieflist/%s' % key)

            self.assertEquals(briefs_cache[key]['length'], len(response.data))
