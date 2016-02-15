from devfun import app
from flask import send_from_directory, render_template

@app.route('/static/<filename>')
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def error_handler(error):
    return render_template('404.html'), 404
