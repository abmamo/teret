# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, abort, current_app
# import flask login functions
from flask_login import current_user, login_user, logout_user
# import user model
from app.mod_auth.models import User
# import db
from app.extensions import db
# send mail functions
from app.mail import send_mail
from app.extensions import mail
# import serializer
from app import ts


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
        user = User.query.filter_by(email=email).first()
        # check user has been found
        if user is None or not user.check_password(password):
            return redirect(url_for('auth.signin'))
        # login user if found
        login_user(user)
        # get next from argument
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '' or next_page == "/":
            next_page = url_for('cms.editor')
        # alert user
        flash("signed in.")
        # return response
        return redirect(url_for('cms.home'))
    # alert user
    flash("please sign in!")
    return render_template("signin.html")


@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_app.config['MAX_USERS_NOT_REACHED']:
        if request.method == 'POST':
            # get data from forms
            email = request.form['email']
            password = request.form['password']
            # find user
            user = User.query.filter_by(email=email).first()
            # check email has been found
            if user != None:
                # return to sign up page
                return redirect(url_for('auth.signup'))
            # initialize user
            user = User(email=email, password=password)
            # add to session
            db.session.add(user)
            db.session.commit()
            db.session.close()
            # prepare email
            subject = "confirm account."
            # generate token
            token = ts.dumps(email, salt='email-confirm-key')
            # build recover url
            confirm_url = url_for(
                'auth.confirm_email',
                token=token,
                _external=True)
            # send the emails
            send_mail(subject, current_app.config['MAIL_USERNAME'],
                      [email], confirm_url)
            # update user count
            current_app.config['MAX_USERS_NOT_REACHED'] = False
            # update user
            flash('account created. confirm email address.')
            # return to login
            return redirect(url_for('auth.signin'))
        return render_template('signup.html')
    flash("signup not active.")
    return redirect(url_for('signin'))


@mod_auth.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    # check validity of token passed using the serializer
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(400)

    try:
        # get the user using the email
        user = User.query.filter_by(email=email).first_or_404()
        # confirm user
        user.confirmed = True
        # save changes in database
        db.session.commit()
        db.session.close()
        # alert user
        flash("email address confirmed.")
        return redirect(url_for('auth.signin'))
    except:
        abort(500)


@mod_auth.route('/reset', methods=['GET', 'POST'])
def request_reset():
    # try:
    if request.method == 'POST':
        # get email from form
        email = request.form['email']
        # query user by emeail
        user = User.query.filter_by(email=email).first()
        # prepare email
        subject = "Password reset requested"
        # generate token
        token = ts.dumps(user.email, salt='recover-key')
        # build recover url
        recover_url = url_for(
            'auth.reset_with_token',
            token=token,
            _external=True)
        # send the email
        send_mail(subject, current_app.config['MAIL_USERNAME'],
                  [email], recover_url)
        # alert user
        flash("reset link sent.")
        return redirect(url_for('base.home'))
    flash("reset password.")
    return render_template("request_reset.html")
    # except:
    # abort(500)


@mod_auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    # check validity of token passed using the serializer
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(400)
    # change password if valid token provided
    if request.method == 'POST':
        # get new password from form
        password = request.form['password']
        # get user using email
        user = User.query.filter_by(email=email).first_or_404()
        # set hashed password in database
        user.set_password(password)
        # save changes in database
        db.session.commit()
        db.session.close()
        # alert user
        flash("password successfully reset.")
        return redirect(url_for('auth.signin'))   
    return render_template('reset_with_token.html', token=token)


@mod_auth.route('/signout')
def signout():
    logout_user()
    flash("signed out.")
    return redirect(url_for('base.home'))
