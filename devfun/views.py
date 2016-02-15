from devfun import app, db, lm
from flask import send_from_directory, render_template, request, flash, redirect, url_for, g
from flask.ext.login import current_user, login_user, login_required, logout_user
from .forms import RegistrationForm, LoginForm
from .models import User

@lm.user_loader
def load_user(id):
    return User.query.get(id)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/static/<filename>')
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.errorhandler(404)
def error_handler(error):
    return render_template('404.html'), 404



@app.route('/')
def index():
    return render_template('index.html', title="DevFun home page!")


@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash(u'Successfully logged in as {}'.format(form.user.username))
        session['user_id'] = form.user.id
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User(form.username.data, form.email.data,
                  form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title="Register Account")
