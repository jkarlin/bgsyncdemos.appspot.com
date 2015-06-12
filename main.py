from flask import Flask
from flask import Response
from flask import json
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

from werkzeug.utils import escape
import cloudstorage as gcs

from google.appengine.api import app_identity

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

def get_filename():
	bucket_name = app_identity.get_default_gcs_bucket_name()
	return '/' + bucket_name + '/post-data'

@app.route('/')
def index():
	return redirect(url_for('oneshot'))

@app.route('/oneshot/')
def oneshot():
	string_json = do_get()
	obj = json.loads(string_json)
	return render_template('index.html', text=obj['text'])

@app.route('/oneshot/oneshot_sw.js')
def oneshot_sw():
	# This needs to be routed through /oneshot/ for service worker scoping
	return send_from_directory('static', 'oneshot_sw.js')

@app.route('/oneshot/get')
def do_get():
	filename = get_filename()

	gcs_file = gcs.open(filename)
	txt = gcs_file.read()
	gcs_file.close()

	return json.dumps({"text": txt})

@app.route('/oneshot/post', methods=['POST'])
def do_post():
	obj = json.loads(request.data)
	txt = escape(obj['text']).encode('utf-8')

	filename = get_filename()
	gcs_file = gcs.open(filename, 'w' )
	gcs_file.write(txt)
	gcs_file.close()

	return do_get()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404