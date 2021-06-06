"""
    controller.py: contains all handlers for cms bp
"""
# import os to remove files
import os

# flask dependencies
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    abort,
)

# import login manager
from flask_login import login_required

# import slug creation libs
from slugify import slugify

# import post model
from app.bps.cms.models import Post

# import db session
from app.extensions import db, uploads

# blueprint
cms = Blueprint("cms", __name__, url_prefix="/cms")


@cms.route("/", methods=["GET"])
@login_required
def home():
    """
    cms dashboard page
    """
    # sort stories by creation date
    stories = Post.query.all()[::-1]
    # get tags
    tags = list({post.tags for post in stories})
    # render cms page
    return render_template(
        "cms.html",
        tags=tags,
        stories=stories,
        app_name=current_app.config["APP_NAME"],
    )


@cms.route("/editor", methods=["GET"])
@login_required
def editor():
    """
    editor page
    """
    # render summernote editor page
    return render_template("editor.html")


@cms.route("/upload", methods=["POST"])
@login_required
def upload():
    """
    upload image
    """
    # image upload url doesn't render anything
    try:
        # try saving image and return url on disk
        image_filename = uploads.save(request.files["image"])
        image_url = uploads.url(image_filename)
        # return image url
        return image_url
    except Exception as error:  # pylint: disable=broad-except
        # log
        current_app.logger.warning("upload failed with: %s" % str(error))
        # if image can't be saved returned empty string as url
        return ""


@cms.route("/save", methods=["POST"])
@login_required
def save():  # pylint: disable=inconsistent-return-statements
    """
    save post
    """
    if request.method == "POST":
        try:
            # get post data from form
            title = request.form["title"]
            slug = slugify(title)
            content = request.form["content"]
            tags = request.form["tags"]
        except Exception as error:  # pylint: disable=broad-except
            # log
            current_app.logger.warning("form data failed with: %s" % str(error))
            # return error page
            abort(500)
        # try and get main image if not just keep it empty
        try:
            image_filename = uploads.save(request.files["image"])
            image_url = uploads.url(image_filename)
        except Exception as error:  # pylint: disable=broad-except
            # log
            current_app.logger.warning("file data failed with: %s" % str(error))
            # set to empty
            image_filename = ""
            image_url = ""
        try:
            # check if post already exists if so update
            if Post.query.filter_by(slug=slug).first():
                post = Post.query.filter_by(slug=slug).first()
                post.title = title
                post.slug = slug
                post.content = content
                post.tags = tags
                post.image_filename = image_filename
                post.image_url = image_url
            else:
                # create post
                post = Post(
                    title=title,
                    slug=slug,
                    content=content,
                    tags=tags,
                    image_filename=image_filename,
                    image_url=image_url,
                )
                # add to database
                db.session.add(post)
            # commit the changes
            db.session.commit()
            db.session.close()
        except Exception as error:  # pylint: disable=broad-except
            # log
            current_app.logger.warning("post create failed with: %s" % str(error))
            # return error page
            abort(500)
        # alert user
        flash("saved.")
        # redirect to cms homepage
        return redirect(url_for("cms.home"))


@cms.route("/edit/<string:slug>", methods=["GET", "POST"])
@login_required
def edit(slug):
    """
    edit post
    """
    # edit specific story
    story = Post.query.filter_by(slug=slug).first()
    # render edit page
    return render_template("edit.html", story=story)


@cms.route("/publish/<string:slug>", methods=["POST"])
@login_required
def publish(slug):
    """
    publish post
    """
    # get post by id
    post = Post.query.filter_by(slug=slug).first()
    # set published to True
    post.published = True
    # commit changes to database
    db.session.commit()
    db.session.close()
    # alert user
    flash("published.")
    return redirect(url_for("cms.home"))


@cms.route("/unpublish/<string:slug>", methods=["POST"])
@login_required
def unpublish(slug):
    """
    unpublish post
    """
    # get post by id
    post = Post.query.filter_by(slug=slug).first()
    # set published to false
    post.published = False
    # commit changes to database
    db.session.commit()
    db.session.close()
    # alert
    flash("unpublished.")
    # redirect
    return redirect(url_for("cms.home"))


@cms.route("/delete/<string:slug>", methods=["POST"])
@login_required
def delete(slug):
    """
    delete post
    """
    # need to add ways to depelete post images
    post = Post.query.filter_by(slug=slug).first()
    post_image_path = os.path.join(
        os.getcwd(), "app/static/images/uploads", post.image_filename
    )
    # if path exists
    if post_image_path:
        # delete the image associated with the post stored on disk
        os.remove(post_image_path)
    # delete post
    db.session.delete(post)
    db.session.commit()
    db.session.close()
    # alert user
    flash("deleted")
    # redirect to cms
    return redirect(url_for("cms.home"))
