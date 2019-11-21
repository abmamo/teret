# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# import login manager
from flask_login import login_required
# import post model
from app.mod_cms.models import Post
# import slug creation libs
from slugify import slugify
# import db session
from app import db, uploads


# Define the blueprint: 'auth', set its url prefix: mod_cms.url/auth
mod_cms = Blueprint('cms', __name__, url_prefix='/cms')

# basic routes
@mod_cms.route('/', methods=['GET'])
@login_required
def home():
    tags = Post.query.distinct(Post.tags).all()
    stories = Post.query.all()
    return render_template('cms.html', tags=tags, stories=stories)

@mod_cms.route('/editor', methods=['GET'])
@login_required
def editor():
    return render_template('editor.html')

@mod_cms.route('/save', methods=['POST'])
@login_required
def save():
    if request.method == 'POST':
        title = request.form['title']
        slug = slugify(title)
        content = request.form['content']
        tags = request.form['tags']
        # try and get images if not just keep it empty
        try:
            image_filename = uploads.save(request.files['image'])
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
            post = Post(title=title, slug=slug, content=content, tags=tags, image_filename = image_filename, image_url = image_url)
            # add to database
            db.session.add(post)
        # commit the changes
        db.session.commit()
        db.session.close()
        return redirect(url_for('cms.home'))

@mod_cms.route('/edit/<string:slug>', methods=['GET', 'POST'])
@login_required
def edit(slug):
    story = Post.query.filter_by(slug=slug).first()
    return render_template('edit.html', story=story)

@mod_cms.route('/publish/<string:slug>', methods=['POST'])
@login_required
def publish(slug):
    post = Post.query.filter_by(slug=slug).first()
    post.published = True
    db.session.commit()
    db.session.close()
    return redirect(url_for('cms.home'))

@mod_cms.route('/unpublish/<string:slug>', methods=['POST'])
@login_required
def unpublish(slug):
    post = Post.query.filter_by(slug=slug).first()
    post.published = False
    db.session.commit()
    db.session.close()
    return redirect(url_for('cms.home'))

@mod_cms.route('/delete/<string:slug>', methods=['POST'])
@login_required
def delete(slug):
    post = Post.query.filter_by(slug=slug).first()
    db.session.delete(post)
    db.session.commit()
    db.session.close()
    return redirect(url_for('cms.home'))

