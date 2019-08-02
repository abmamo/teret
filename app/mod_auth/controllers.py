# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
# import flask login functions
from flask_login import current_user, login_user, logout_user
# import user model
from app.mod_auth.models import User
# import db
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # get form values
        email = request.form['email']
        password = request.form['password']
        # find user
        user = User.query.filter_by(email = email).first()
        # check user has been found
        if user is None or not user.check_password(password):
            return redirect(url_for('auth.signin'))
        # login user if found
        login_user(user)
        # get next from argument
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '' or next_page == "/":
            next_page = url_for('cms.editor')
        return redirect(url_for('cms.home'))
    flash("You need to sign in!")
    return render_template("signin.html")

@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get data from forms
        email = request.form['email']
        password = request.form['password']
        # initialize user
        user = User(email=email)
        user.set_password(password)
        # add to session
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return redirect(url_for('auth.signin'))
    return render_template('signup.html')

@mod_auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('base.home'))


