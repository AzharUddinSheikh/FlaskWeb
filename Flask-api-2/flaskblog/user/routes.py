from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Posts
from flaskblog.user.form import RegistrationForm, LoginForm, UpdateAccountForm, RequestForm, ResetPasswordForm
from flaskblog.user.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your Account Has Been Created Now you are able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            
            next_page = request.args.get('next')

            flash('You have been Logged in','success')
            return redirect(url_for('users.account')) if next_page else redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessful Please check email and Password', 'danger')

    return render_template('/login.html', title='Register', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash('Logout Successfully','success')
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

# updating picture username and email if post
        if form.picture.data:
            picture_file  = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated','success')
        return redirect(url_for('users.account'))

    # if you want to show current data without req post method  in the input field of account then
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    imagefile = url_for('static',filename='img/'+current_user.image_file)
    #image_file is the column name in User table check out models with the help of current user we can access to exact location if we dont then sql ll rise error
    return render_template('account.html',title='Account', imagefile=imagefile, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query\
            .filter_by(author=user)\
            .order_by(Posts.date_posted.desc())\
            .paginate(per_page=5,page=page)
    return render_template('user_posts.html',posts=posts,user=user)


@users.route('/reset_password',methods=['GET','POST'])
def reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instruction to reset password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title="Reset Password",form=form)


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token or expired token', 'warning')
        return "redirect(url_for('users.reset_request'))"

    form = ResetPasswordForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash('Your Password has been Recovered Now you are able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password',form=form)

