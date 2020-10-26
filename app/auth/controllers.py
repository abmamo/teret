# flask
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    session,
    redirect,
    url_for,
    abort,
    current_app,
)
# url parsing
from urllib.parse import urlparse

# auth
from flask_login import current_user, login_user, logout_user

# db model
from app.auth.models import User

# db extension
from app.extensions import db

# send mail functions
from app.mail import send_mail
from app.extensions import mail

# import serializer
from app.factory import ts


# auth module
auth = Blueprint("auth", __name__, url_prefix="/")

# Set the route and accepted methods
@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        try:
            # get form values
            email = request.form["email"]
            password = request.form["password"]
        except Exception as e:
                # log
                current_app.logger.warning("getting request data failed with: %s" % str(e))
                # return error page
                abort(500)
        try:
            # find user
            user = User.query.filter_by(email=email).first()
            # check user has been found
            if user is None or not user.check_password(password):
                # alert user
                flash("invalid credentials")
                # redirect to sign in page
                return redirect(url_for("auth.signin"))
        except Exception as e:
                # log
                current_app.logger.warning("exists validation failed with: %s" % str(e))
                # return error page
                abort(500)
        try:
            # login user if found
            login_user(user)
            # get next from argument
            next_page = request.args.get("next")
            # check if there is next page in url
            if not next_page or urlparse(next_page).netloc != "" or next_page == "/":
                next_page = url_for("cms.home")
        except Exception as e:
            # log
            current_app.logger.warning("sign in failed with: %s" % str(e))
            # return error page
            abort(500)
        # alert user
        flash("signed in")
        # return response
        return redirect(next_page)
    # return sign in page
    return render_template("signin.html")

@auth.route("/confirm/<token>", methods=["GET", "POST"])
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
        flash("email confirmed")
        # return to signin page
        return redirect(url_for("auth.signin"))
    except:
        # log
        current_app.logger.warning("confirm failed")
        # return error page
        abort(500)


@auth.route("/reset", methods=["GET", "POST"])
def request_reset():
    if request.method == "POST":
        try:
            # get email from form
            email = request.form["email"]
        except Exception as e:
            # log
            current_app.logger.warning("getting request data failed with: %s" % str(e))
            # return error page
            abort(500)
        try:
            # query user by emeail
            user = User.query.filter_by(email=email).first()
            # check if user has been found
            if user is None:
                # alert user
                flash("invalid credentials")
                # return to reset page
                return render_template("request_reset.html")
        except Exception as e:
                # log
                current_app.logger.warning("exists validation failed with: %s" % str(e))
                # return error page
                abort(500)
        try:
            # prepare email
            subject = "password reset requested"
            # generate token
            token = ts.dumps(user.email, salt="recover-key")
            # build recover url
            recover_url = url_for("auth.reset_with_token", token=token, _external=True)
            # send the email
            send_mail(subject, current_app.config["MAIL_USERNAME"], [email], recover_url)
        except Exception as e:
            # log
            current_app.logger.warning("send reset failed with: %s" % str(e))
            # return error page
            abort(500)
        # alert user
        flash("reset link sent")
        # redirect to home
        return redirect(url_for("base.home"))
    return render_template("request_reset.html")


@auth.route("/reset/<token>", methods=["GET", "POST"])
def reset_with_token(token):
    # check validity of token passed using the serializer
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(400)
    # change password if valid token provided
    if request.method == "POST":
        try:
            # get new password from form
            password = request.form["password"]
        except Exception as e:
            # log
            current_app.logger.warning("getting request data failed with: %s" % str(e))
            # return error page
            abort(500)
        try:
            # get user using email
            user = User.query.filter_by(email=email).first_or_404()
            # set hashed password in database
            user.set_password(password)
            # save changes in database
            db.session.commit()
            db.session.close()
        except Exception as e:
                # log
                current_app.logger.warning("password reset failed with: %s" % str(e))
                # return error page
                abort(500)
        # alert user
        flash("password successfully reset.")
        # redirect to sign in
        return redirect(url_for("auth.signin"))
    return render_template("reset_with_token.html", token=token)


@auth.route("/signout")
def signout():
    # log out user
    logout_user()
    # alert user
    flash("signed out")
    # redirect to home
    return redirect(url_for("base.home"))
