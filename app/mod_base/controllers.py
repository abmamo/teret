# flask
from flask import Blueprint, render_template, abort, current_app

# db models
from app.mod_cms.models import Post

# blueprint
mod_base = Blueprint("base", __name__, url_prefix="/")

# basic routes
@mod_base.route("/", methods=["GET"])
def home():
    try:
        # render the home page
        return render_template("home.html")
    except Exception as e:
        # log
        current_app.logger.warning("home failed.")
        # render error page
        abort(500)


@mod_base.route("/stories", methods=["GET"])
def stories():
    try:
        # server side render of tags and stories
        tags = Post.query.filter_by(published=True).distinct(Post.tags).all()
        # sort stories by latest
        stories = Post.query.filter_by(published=True).all()[::-1]
        # render stories page
        return render_template("stories.html", tags=tags, stories=stories)
    except Exception as e:
        # log
        current_app.logger.warning("stories failed.")
        # render error page
        abort(500)


@mod_base.route("/about", methods=["GET"])
def about():
    try:
        # render about page
        return render_template("about.html")
    except Exception as e:
        # log
        current_app.logger.warning("about failed.")
        # render error page
        abort(500)
