"""
    controller.py: contains all handlers for auth bp
"""
# url parsing
from urllib.parse import urlparse

# flask
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    abort,
    current_app,
)

# auth
from flask_login import login_user, logout_user

# db model
from app.bps.auth.models import User

# db extension
from app.extensions import db, login

# send mail functions
from app.mail import send_mail

# import serializer
from app.extensions import ts


# auth module
auth = Blueprint("auth", __name__, url_prefix="/")

# initialise login manager
@login.user_loader
def load_user(user_id):
    """
    user loader
    """
    return User.query.get(int(user_id))


# Set the route and accepted methods
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    """
    sign in page
    """
    if request.method == "POST":
        # get form values
        email = request.form["email"]
        password = request.form["password"]
        # find user
        user = User.query.filter_by(email=email).first()
        # check user has been found
        if user is None or not user.check_password(password):
            # alert user
            flash("invalid credentials")
            # redirect to sign in page
            return redirect(url_for("auth.signin"))
        # login user if found
        login_user(user)
        # get next from argument
        next_page = request.args.get("next")
        # check if there is next page in url
        if not next_page or urlparse(next_page).netloc != "" or next_page == "/":
            next_page = url_for("cms.home")
        # alert user
        flash("signed in")
        # return response
        return redirect(next_page)
    # return sign in page
    return render_template("signin.html")


@auth.route("/confirm/<token>", methods=["GET", "POST"])
def confirm_email(token):
    """
    confirm email page
    """
    # check validity of token passed using the serializer
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:  # pylint: disable=bare-except
        abort(400)
    # get the user using the email
    user = User.query.filter_by(email=email).first_or_404()
    # confirm user
    user.confirmed = True
    # save changes in database
    db.session.commit()
    db.session.close()
    # alert user
    flash("email confirmed")
    # return to signin page
    return redirect(url_for("auth.signin"))


@auth.route("/reset", methods=["GET", "POST"])
def request_reset():
    """
    request rest page
    """
    if request.method == "POST":
        # get email from form
        email = request.form["email"]
        # query user by emeail
        user = User.query.filter_by(email=email).first()
        # check if user has been found
        if user is None:
            # alert user
            flash("invalid credentials")
            # return to reset page
            return render_template("reset.html")
        # prepare email
        subject = "password reset requested"
        # generate token
        token = ts.dumps(user.email, salt="recover-key")
        # build recover url
        recover_url = url_for("auth.reset_with_token", token=token, _external=True)
        # send the email
        send_mail(subject, current_app.config["MAIL_USERNAME"], [email], recover_url)
        # alert user
        flash("reset link sent")
        # redirect to home
        return redirect(url_for("base.home")), 302
    return render_template("reset.html")


@auth.route("/reset/<token>", methods=["GET", "POST"])
def reset_with_token(token):
    """
    reset password with token
    """
    # check validity of token passed using the serializer
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:  # pylint: disable=bare-except
        abort(400)
    # change password if valid token provided
    if request.method == "POST":
        # get new password from form
        password = request.form["password"]
        # get user using email
        user = User.query.filter_by(email=email).first_or_404()
        # set hashed password in database
        user.set_password(password)
        # save changes in database
        db.session.commit()
        db.session.close()
        # alert userw
        flash("password successfully reset")
        # redirect to sign in
        return redirect(url_for("auth.signin"))
    return render_template("change.html", token=token)


@auth.route("/signout")
def signout():
    """
    sign out user
    """
    # log out user
    logout_user()
    # alert user
    flash("signed out")
    # redirect to home
    return redirect(url_for("base.home"))
