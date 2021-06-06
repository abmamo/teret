"""
    controller.py: contains all handlers for base bp
"""
# flask
from flask import (
    Blueprint,
    render_template,
    current_app,
    flash,
    redirect,
    url_for,
)

# db models
from app.bps.cms.models import Post

# blueprint
base = Blueprint("base", __name__, url_prefix="/")


# basic route
@base.route("/", methods=["GET"])
def home():
    """
    home page
    """
    # sort stories by latest
    stories = Post.query.filter_by(published=True).all()[::-1]
    # get tags
    tags = list({post.tags for post in stories})
    # render stories page
    return render_template(
        "stories.html",
        tags=tags,
        stories=stories,
        app_name=current_app.config["APP_NAME"],
    )


@base.route("/<slug>", methods=["GET"])
def story(slug):
    """
    story page
    """
    # get story by slug
    stry = Post.query.filter_by(slug=slug).first()
    # if story has been found
    if stry is not None:
        # render story
        return render_template(
            "story.html", story=stry, app_name=current_app.config["APP_NAME"]
        )
    # alert user
    flash("story not found")
    # redirect to homepage
    return redirect(url_for("base.home"))
