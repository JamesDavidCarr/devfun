from devfun import app, db, lm
from flask import send_from_directory, render_template, request, flash, redirect, url_for, g
from flask.ext.login import current_user, login_user, login_required, logout_user
from .forms import RegistrationForm, LoginForm, PostForm, CommentForm
from .models import User, Post, Comment

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
@login_required
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
    flash('Errors in your form')
    return render_template('register.html', form=form, title="Register Account")


@app.route('/')
def index():
    return render_template('index.html', title="DevFun home page!")



@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = g.user.username
        post = Post(username, form.title.data, form.url.data)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('view_post', id=post.id))
    return render_template('new_post.html', form=form, title="Create a new post")


@app.route('/post/<id>')
def view_post(id):
    post = Post.query.get(int(id))
    if not post:
        return error_handler()
    else:
        comments = Comment.query.filter(Comment.post == int(id))
        form = CommentForm()
        return render_template('post.html', post=post, comments=comments, title=post.title, form=form, id=post.id)


@app.route('/posts/mine')
@login_required
def view_my_posts():
    username = g.user.username
    posts = Post.query.filter(Post.creator == username).limit(10)
    return render_template('my_posts.html', posts=posts, title="My posts")


@app.route('/posts')
def posts():
    posts = Post.query.limit(10)
    return render_template('posts.html', posts=posts, title="All posts!")


@app.route('/comment/new/<post_id>', methods=['GET', 'POST'])
@login_required
def create_comment(post_id):
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        username = g.user.username

        comment = Comment(username, post_id, form.content.data)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('view_post', id=post_id))
    return url_for('index')
