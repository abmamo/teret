# Import flask dependencies
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
)

# import login manager
from flask_login import login_required

# import post model
from app.mod_cms.models import Post

# import slug creation libs
from slugify import slugify

# import db session
from app.extensions import db
from app import uploads

# import os to remove files
import os


# Define the blueprint: 'auth', set its url prefix: mod_cms.url/auth
mod_cms = Blueprint("cms", __name__, url_prefix="/cms")

# basic routes
@mod_cms.route("/", methods=["GET"])
@login_required
def home():
    # get tags and stories
    tags = Post.query.distinct(Post.tags).all()
    # sort stories by creation date
    stories = Post.query.all()[::-1]
    return render_template("cms.html", tags=tags, stories=stories)


@mod_cms.route("/editor", methods=["GET"])
@login_required
def editor():
    # render summernote editor page
    return render_template("editor.html")


@mod_cms.route("/upload", methods=["POST"])
@login_required
def upload():
    # image upload url doesn't render anything
    try:
        # try saving image and return url on disk
        image_filename = uploads.save(request.files["image"])
        image_url = uploads.url(image_filename)
        return image_url
    except:
        # if image can't be saved returned empty string as url
        return ""


@mod_cms.route("/save", methods=["POST"])
@login_required
def save():
    if request.method == "POST":
        # get post data from form
        title = request.form["title"]
        slug = slugify(title)
        content = request.form["content"]
        tags = request.form["tags"]
        # try and get main image if not just keep it empty
        try:
            image_filename = uploads.save(request.files["image"])
            image_url = uploads.url(image_filename)
        except:
            image_filename = ""
            image_url = ""
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
        # alert user
        flash("saved.")
        # redirect to cms homepage
        return redirect(url_for("cms.home"))


@mod_cms.route("/edit/<string:slug>", methods=["GET", "POST"])
@login_required
def edit(slug):
    # edit specific story
    story = Post.query.filter_by(slug=slug).first()
    return render_template("edit.html", story=story)


@mod_cms.route("/publish/<string:slug>", methods=["POST"])
@login_required
def publish(slug):
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


@mod_cms.route("/unpublish/<string:slug>", methods=["POST"])
@login_required
def unpublish(slug):
    # get post by id
    post = Post.query.filter_by(slug=slug).first()
    # set published to false
    post.published = False
    # commit changes to database
    db.session.commit()
    db.session.close()
    flash("unpublished.")
    return redirect(url_for("cms.home"))


@mod_cms.route("/delete/<string:slug>", methods=["POST"])
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
