# flask
from flask import Blueprint, render_template, abort, current_app

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
