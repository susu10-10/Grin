from flask import render_template, flash, redirect, url_for, request
from grin import app, db
from grin.forms import LoginForm, RegisterForm
from flask_login import current_user, login_required, login_user, logout_user
from grin.models import User


@app.route('/')
@app.route('/index')
def grinhome():
    return render_template('index.html')


@app.route('/register/', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(fullname=form.fullname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route('/login/', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(password=form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        else:
            flash(f'Login successful ', 'success')
            return redirect(url_for('homepage'))
    return render_template('login.html', form=form)


@app.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html')


@app.route('/logout/')
def logout():
    logout_user()
    flash('logout successfully', 'success')
    return redirect(url_for('grinhome'))

@app.route('/account/')
@login_required
def account():
    user = User.query.filter_by().first_or_404()


