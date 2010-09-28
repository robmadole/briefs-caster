import os
import re
import tempfile
import time
import hashlib
from subprocess import Popen, PIPE
from os.path import join, basename, getsize, getmtime, dirname

from jinja2 import Template

from briefscaster import config, get_briefs_utils

_briefs_cache = {}   # The last discovered brieflists

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


def find_briefs(directory):
    """
    Walks through a directory and returns a list of all files ending in
    '.brieflist'.  This will provide absolute paths to these files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            absolute_filename = join(root, file)
            if absolute_filename.endswith('.bs'):
                yield absolute_filename


def get_briefs_cache():
    """
    Accessor for the last generated briefs cache
    """
    return _briefs_cache


def create_brieflist(brief):
    """
    Creates a brieflist from a brief script.  This uses the bs and
    compact-briefs utilities found in the briefscaster/bin directory.
    """
    bs_binary, compact_briefs_binary = get_briefs_utils()

    # Change directories where the brief is
    os.chdir(dirname(brief))

    try:
        plist = open(re.sub('\.bs$', '.plist', brief), 'w')
        brieflist = open(re.sub('\.bs$', '.brieflist', brief), 'w')

        p_bs = Popen("%s %s" % (bs_binary, basename(brief)), shell=True,
                 stdout=plist)
        status = os.waitpid(p_bs.pid, 0)

        # The compact briefs script needs to be relative to the images that it
        # uses, so we are in the proper directory and will use the base file
        # names instead of absolute paths
        p_compact = Popen("%s %s %s" % (compact_briefs_binary,
            basename(plist.name), basename(brieflist.name)),
            shell=True, stdout=PIPE, stderr=PIPE)
        status = os.waitpid(p_compact.pid, 0)

        errors = p_compact.stderr.read()
        if errors:
            print errors
    finally:
        plist.close()
        brieflist.close()

    return brieflist.name


def create_briefs_cache(items, url_root):
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

        item_brieflist = create_brieflist(item)

        value = {
            'bs_filename': item,
            'filename': item_brieflist,
            'title': basename(item_brieflist),
            'url': '%sbrieflist/%s' % (url_root, key,),
            'length': getsize(item_brieflist),
            'description': 'Output from %s' % basename(item),
            'pub_date': pub_date_gmt,
            'guid': key}
        cache[key] = value
    return cache


def create_feed(items, url_root):
    """
    Creates an RSS feed from a list of items where each item is an absolute
    path to a .brieflist file
    """
    global _briefs_cache
    _briefs_cache = create_briefs_cache(items, url_root)

    t_kwargs = {
        'title':
            'Briefs caster server on %s' % url_root,
        'description':
            'Serving up some fine briefs from %s' % config['working_directory'],
        'url_root': url_root,
        'pub_date': time.strftime(GMT_FORMAT, time.gmtime()),
        'items': _briefs_cache}

    template = Template(RSS_TEMPLATE)

    return template.render(**t_kwargs)
