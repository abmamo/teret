# flask
from flask import Blueprint, render_template, abort, current_app, flash, redirect, url_for

# db models
from app.cms.models import Post

# blueprint
base = Blueprint("base", __name__, url_prefix="/")



# basic route
@base.route("/", methods=["GET"])
def home():
    try:
        # sort stories by latest
        stories = Post.query.filter_by(published=True).all()[::-1]
        # get tags
        tags = list(set([post.tags for post in stories]))
        # render stories page
        return render_template("stories.html", tags=tags, stories=stories, app_name=current_app.config["APP_NAME"])
    except Exception as e:
        # log
        current_app.logger.warning("stories failed with: %s" % str(e))
        # render error page
        abort(500)

@base.route("/<slug>", methods=["GET"])
def story(slug):
    # get story by slug
    story = Post.query.filter_by(slug=slug).first()
    # if story has been found
    if story is not None:
        # render story
        return render_template("story.html", story=story, app_name=current_app.config["APP_NAME"])
    # otherwise story not found in db with given slug
    else:
        # alert user
        flash("story not found")
        # redirect to homepage
        return redirect(url_for('base.home'))