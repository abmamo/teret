# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
#import post model for querying stories
from app.mod_auth.models import Post

# Define the blueprint: 'auth', set its url prefix: mod_base.url/auth
mod_base = Blueprint('base', __name__, url_prefix='/')

# basic routes
@mod_base.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@mod_base.route('/stories', methods=['GET'])
def stories():
    tags = Post.query.filter_by(published=True).distinct(Post.tags).all()
    stories = Post.query.filter_by(published=True).all()
    return render_template('stories.html', tags = tags, stories = stories)

@mod_base.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@mod_base.route('/music', methods=['GET'])
def music():
     return render_template('music.html')
