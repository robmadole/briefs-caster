import os
import time
import hashlib
from os.path import join, basename, getsize, getmtime

from jinja2 import Template

from briefscaster import config

_briefslist_cache = {}   # The last discovered brieflists

RSS_TEMPLATE = """
<?xml version="1.0"?>
<rss version="2.0">
    <channel>
        <title>{{ title }}</title>
        <link>{{ url_root }}</link>
        <description>{{ description }}</description>
        <language>en-us</language>
        <pubDate>{{ pub_date }}</pubDate>
        <lastBuildDate>{{ pub_date }}</lastBuildDate>
        {% for key in items %}
            {% set item = items[key] %}
            <item>
                <title>{{ item['title'] }}</title>
                <enclosure url="{{ item['url'] }}" length="{{ item['length'] }}" type="application/brief" />
                <description>{{ item['description'] }}</description>
                <pubDate>{{ item['pub_date'] }}</pubDate>
                <guid>{{ item['guid'] }}</guid>
            </item>
        {% endfor %}
    </channel>
</rss>
""".strip()

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def find_brieflists(directory):
    """
    Walks through a directory and returns a list of all files ending in
    '.brieflist'.  This will provide absolute paths to these files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            absolute_filename = join(root, file)
            if absolute_filename.endswith('.brieflist'):
                yield absolute_filename


def get_brieflist_cache():
    """
    Accessor for the last generated brieflists cache
    """
    return _briefslist_cache


def create_brieflist_cache(items, url_root):
    """
    Creates a lookup cache with a unique key and various information about the
    brieflist as the value. This can be used later on whenever we are serving
    the file.
    """
    cache = {}
    for item in items:
        with open(item) as f:
            hash = hashlib.sha1()
            hash.update(f.read())
            key = hash.hexdigest()

        pub_date = time.gmtime(getmtime(item))
        pub_date_gmt = time.strftime(
            GMT_FORMAT, pub_date)

        value = {
            'filename': item,
            'title': basename(item),
            'url': '%sbrieflist/%s' % (url_root, key,),
            'length': getsize(item),
            'description': item,
            'pub_date': pub_date_gmt,
            'guid': key}
        cache[key] = value
    return cache


def create_feed(items, url_root):
    """
    Creates an RSS feed from a list of items where each item is an absolute
    path to a .brieflist file
    """
    global _briefslist_cache
    _briefslist_cache = create_brieflist_cache(items, url_root)

    t_kwargs = {
        'title':
            'Briefs caster server on %s' % url_root,
        'description':
            'Serving up some fine briefs from %s' % config['working_directory'],
        'url_root': url_root,
        'pub_date': time.strftime(GMT_FORMAT, time.gmtime()),
        'items': _briefslist_cache}

    template = Template(RSS_TEMPLATE)

    return template.render(**t_kwargs)
