from devfun import app, db, lm
from flask import send_from_directory, render_template, request, flash, redirect, url_for, g
from flask.ext.login import current_user, login_user, login_required
from .forms import LoginForm
from .models import User

@lm.user_loader
def load_user(id):
    print "Got here LOGLOGLOG"
    return User.query.get(id)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/static/<filename>')
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/')
@login_required
def index():
    return render_template('index.html', title="DevFun home page!")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                  form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title="Register Account")


@app.errorhandler(404)
def error_handler(error):
    return render_template('404.html'), 404
