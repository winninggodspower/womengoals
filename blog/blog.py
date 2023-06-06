from flask import Blueprint, render_template, request, redirect, flash
from .auth import auth
from .forms import BlogForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import os
from .db import Post, db

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
blog = Blueprint('blog', __name__, url_prefix='/blog')

class BlogConfig:
    def __init__(self, app) -> None:
        ckeditor = CKEditor(app)

@blog.route("/create_blog", methods=['GET', 'POST'])
@auth.login_required
def create_blog():
    form = BlogForm()
    if form.validate_on_submit():
        image_path = save_blog_image(form.image.data) # save blog image
        post = Post(title=form.title.data, intro=form.intro.data, content=form.content.data, image=image_path)
        db.session.add(post)
        db.session.commit()
        
        flash("successfully added a blog", 'success')
        return redirect('/blog/create_blog')
    
    
    return render_template("blog/create_blog.html", form=form)

@blog.route("", methods=['GET', 'POST'])
@auth.login_required
def view_all_blog():
    all_blogs = Post.query.all()
    return render_template("blog/view_all_blog.html", all_blog=all_blogs)


def save_blog_image(f ):
    filename = secure_filename(f.filename)
    BLOG_PHOTO_DIR = os.path.join(PROJECT_DIR, 'photos')

    # create blog photo directory if it doesnt exist
    if not os.path.exists(BLOG_PHOTO_DIR):
        print("photo directory exists")
        os.makedirs(BLOG_PHOTO_DIR)
    
    # get full blog_path
    file_path = os.path.join(
        PROJECT_DIR, 'photos', filename
    )
    f.save(file_path)

    return file_path

