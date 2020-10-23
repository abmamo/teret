# Import flask dependencies
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    session,
    redirect,
    url_for,
    current_app,
    abort
)

# import login manager
from flask_login import login_required

# import post model
from app.cms.models import Post

# import slug creation libs
from slugify import slugify

# import db session
from app.extensions import db
from app.factory import uploads

# import os to remove files
import os


# blueprint
cms = Blueprint("cms", __name__, url_prefix="/cms")

# basic routes
@cms.route("/", methods=["GET"])
@login_required
def home():
    try:
        # get tags and stories
        tags = Post.query.distinct(Post.tags).all()
        # sort stories by creation date
        stories = Post.query.all()[::-1]
        # render cms page
        return render_template("cms.html", tags=tags, stories=stories)
    except Exception as e:
        # log
        current_app.logger.warning("dashboard failed.")
        # return error page
        abort(500)

@cms.route("/editor", methods=["GET"])
@login_required
def editor():
    try:
        # render summernote editor page
        return render_template("editor.html")
    except Exception as e:
        # log
        current_app.logger.warning("editor failed.")
        # return error page
        abort(500)


@cms.route("/upload", methods=["POST"])
@login_required
def upload():
    # image upload url doesn't render anything
    try:
        # try saving image and return url on disk
        image_filename = uploads.save(request.files["image"])
        image_url = uploads.url(image_filename)
        return image_url
    except:
        # log
        current_app.logger.warning("upload failed.")
        # if image can't be saved returned empty string as url
        return ""


@cms.route("/save", methods=["POST"])
@login_required
def save():
    if request.method == "POST":
        try:
            # get post data from form
            title = request.form["title"]
            slug = slugify(title)
            content = request.form["content"]
            tags = request.form["tags"]
        except Exception as e:
            # log
            current_app.logger.warning("form data failed.")
            # return error page
            abort(500)
        # try and get main image if not just keep it empty
        try:
            image_filename = uploads.save(request.files["image"])
            image_url = uploads.url(image_filename)
        except Exception as e:
            # log
            current_app.logger.warning("file data failed.")
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
        except Exception as e:
            # log
            current_app.logger.warning("post create failed.")
            # return error page
            abort(500)
        # alert user
        flash("saved.")
        # redirect to cms homepage
        return redirect(url_for("cms.home"))


@cms.route("/edit/<string:slug>", methods=["GET", "POST"])
@login_required
def edit(slug):
    try:
        # edit specific story
        story = Post.query.filter_by(slug=slug).first()
        # render edit page
        return render_template("edit.html", story=story)
    except Exception as e:
        # log
        current_app.logger.warning("edit failed.")
        # return error page
        abort(500)


@cms.route("/publish/<string:slug>", methods=["POST"])
@login_required
def publish(slug):
    try:
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
    except Exception as e:
        # log
        current_app.logger.warning("publish failed.")
        # return error page
        abort(500)


@cms.route("/unpublish/<string:slug>", methods=["POST"])
@login_required
def unpublish(slug):
    try:
        # get post by id
        post = Post.query.filter_by(slug=slug).first()
        # set published to false
        post.published = False
        # commit changes to database
        db.session.commit()
        db.session.close()
        flash("unpublished.")
        return redirect(url_for("cms.home"))
    except Exception as e:
        # log
        current_app.logger.warning("unpublish failed.")
        # return error page
        abort(500)


@cms.route("/delete/<string:slug>", methods=["POST"])
@login_required
def delete(slug):
    # need to add ways to depelete post images
    post = Post.query.filter_by(slug=slug).first()
    try:
        path = os.path.join(
            os.getcwd(), "app/static/images/uploads", post.image_filename
        )
        # delete the image associated with the post stored on disk
        os.remove(path)
    except:
        pass
    db.session.delete(post)
    db.session.commit()
    db.session.close()
    flash("deleted.")
    return redirect(url_for("cms.home"))
