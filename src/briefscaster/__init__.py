import sys
import os

from flask import Flask, request, abort

app = Flask(__name__)

config = {
    'working_directory': os.getcwd(),
    'always_regenerate': True}


@app.route('/')
def provide_briefcast():
    from briefscaster import briefcast

    url_root = request.url_root
    items = briefcast.find_briefs(config['working_directory'])

    rss_string = briefcast.create_feed(
        items,
        url_root)

    return app.response_class(rss_string,
        mimetype='application/briefcast')


@app.route('/brieflist/<key>')
def brieflist(key):
    from briefscaster import briefcast

    briefs_cache = briefcast.get_briefs_cache()

    if not key in briefs_cache:
        abort(404)

    if config['always_regenerate']:
        briefcast.create_brieflist(briefs_cache[key]['bs_filename'])

    filename = briefs_cache[key]['filename']

    with open(filename) as f:
        return app.response_class(f.read(), mimetype='application/brief')


def main():
    try:
        config['working_directory'] = sys.argv[1]
    except IndexError:
        pass

    print 'briefs-caster - Serving up some fine briefs for you\n'
    print 'Open http://<IP_ADDRESS>:5000 from the Briefs app\n'

    print 'CTRL-C to exit the server'
    app.run('0.0.0.0')

if __name__ == '__main__':
    main()
