from devfun import app, db
from flask import send_from_directory, render_template, request, flash, redirect, url_for
from .forms import LoginForm
from .models import User

@app.route('/static/<filename>')
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/')
def index():
    return render_template('index.html', title="DevFun home page!")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                  form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title="Register Account")


@app.errorhandler(404)
def error_handler(error):
    return render_template('404.html'), 404
