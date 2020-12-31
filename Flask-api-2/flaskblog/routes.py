from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.form import RegistrationForm, LoginForm
from flaskblog.models import User, Posts
from flask_login import login_user, current_user, logout_user

posts = [
    {
        'author': 'Azhar',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'December 28,2020'
    },
    {
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'December 29,2020'
    }
]


@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your Account Has Been Created Now you are able to login', 'success')
        return redirect(url_for('home'))
    return render_template('/register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You have been Logged in','success')
            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful Please check email and Password', 'danger')

    return render_template('/login.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout Successfully','success')
    return redirect(url_for('home'))