import sys
import os

from flask import Flask, request, abort

app = Flask(__name__)

config = {
    'working_directory': os.getcwd()}


@app.route('/')
def provide_briefcast():
    from briefscaster import briefcast

    url_root = request.url_root
    items = briefcast.find_brieflists(config['working_directory'])

    rss_string = briefcast.create_feed(
        items,
        url_root)

    return app.response_class(rss_string,
        mimetype='application/briefcast')


@app.route('/brieflist/<key>')
def brieflist(key):
    from briefscaster import briefcast

    brieflist_cache = briefcast.get_brieflist_cache()

    if not key in brieflist_cache:
        abort(404)

    filename = brieflist_cache[key]['filename']

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
