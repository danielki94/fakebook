from flask_login.utils import login_required
from .import bp as app
from app import db
from flask import render_template, url_for, request, redirect, flash
from .models import User
from flask_login import login_user, logout_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        emailData = request.form.get('email')
        passwordData = request.form.get('password')

        # if email and password match what's in the database
        user = User.query.filter_by(email=emailData).first()
        if user is None or not user.check_password(passwordData):
            return redirect(url_for('authentication.login'))
        login_user(user)
        flash('User logged in successfully.', 'success')
        return redirect(url_for('main.home'))
    return render_template('authentication/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # confirm they're in db
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        # if yes
        if user is not None:
            # send message to let us know and redirect back to register route
            flash('That user already exists. Try again.', 'danger')
            return redirect(url_for('authentication.register'))
            # if they don't match
        if request.form.get('password') != request.form.get('confirm_password'):
            flash('Your passwords don\'t match. Try again', 'danger')
            return redirect(url_for('authentication.register'))
        u = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email')
        )
        u.create_password_hash(request.form.get('password'))
        u.save()
        flash('User registered successfully', 'success')
        return redirect(url_for('authentication.login'))
    return render_template('authentication/register.html')
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User logged out successfully.', 'warning')
    return redirect(url_for('authentication.login'))

