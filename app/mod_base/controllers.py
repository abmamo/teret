# Import flask dependencies
from flask import Blueprint, render_template

# import post model for querying stories
from app.mod_cms.models import Post

# Define the blueprint: 'auth', set its url prefix: mod_base.url/auth
mod_base = Blueprint("base", __name__, url_prefix="/")

# basic routes
@mod_base.route("/", methods=["GET"])
def home():
    # render the home page
    return render_template("home.html")


@mod_base.route("/stories", methods=["GET"])
def stories():
    # server side render of tags and stories
    tags = Post.query.filter_by(published=True).distinct(Post.tags).all()
    # sort stories by latest
    stories = Post.query.filter_by(published=True).all()[::-1]
    # render stories page
    return render_template("stories.html", tags=tags, stories=stories)


@mod_base.route("/about", methods=["GET"])
def about():
    # render about page
    return render_template("about.html")
