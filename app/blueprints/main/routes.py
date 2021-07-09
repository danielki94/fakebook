from flask import render_template, request, url_for
from flask.helpers import flash
from werkzeug.utils import redirect
from .import bp as app
from flask_login import current_user
from app import db
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        u = User.query.get(current_user.id)
        u.post = Post.query.filter_by(body=request.form.get('body_text')).first()
        u.post = Post(body = request.form.get('body_text'), user_id=current_user.id)
        u.post.save()
        flash('You added a new post!', 'success')
        return redirect(url_for('main.home'))
    print(current_user.followed_posts)
    context = {
        'posts': current_user.followed_posts() if current_user.is_authenticated else []
    }
    return render_template('home.html', **context)

# @app.route('/', methods=['GET', 'POST'])
# def create_post():
#     if request.method == 'POST':
#         u = User.query.get(current_user.id)
#         u.post = Post.query.filter_by(body=request.form.get('body_text')).first()
#         u.post = Post(body = request.form.get('body_text'), user_id=current_user.id)
#         u.post.save()
#         flash('You added a new post!', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('home.html')


# profile

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        u = User.query.get(current_user.id)
        u.first_name = request.form.get('first_name')
        u.last_name = request.form.get('last_name')
        u.email = request.form.get('email')
        db.session.commit()
        flash('Profile updated successfully', 'info')
        return redirect(url_for('main.profile'))
    # return render_template('profile.html')

    context = {
        "posts": current_user.own_posts()
    }
    return render_template('profile.html', **context)


# contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

