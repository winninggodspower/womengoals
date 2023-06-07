from flask import Blueprint, render_template, request, redirect, flash
from .auth import auth
from .forms import BlogForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import os
from .models import Post, db
from flask import current_app

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
blog = Blueprint('blog', __name__, url_prefix='/blog')

class BlogConfig:
    def __init__(self, app) -> None:
        app.config["UPLOAD_FOLDER"] = os.getenv('UPLOAD_FOLDER')
        ckeditor = CKEditor(app)



@blog.route("/", methods=['GET', 'POST'])
def view_all_blog():
    print(bool(auth.username()))
    all_blogs = Post.query.all()
    return render_template("blog/view_all_blog.html", all_blogs=all_blogs, user_is_authenticated=bool(auth.username()))


@blog.route('/<string:blog_slug>')
def view_blog(blog_slug):
    blog = Post.query.filter_by(slug=blog_slug).first_or_404()
    return render_template('blog/view_blog.html', blog=blog, user_is_authenticated = auth.current_user)


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


@blog.route("/edit_post/<string:blog_title>", methods=["GET", "POST"])
def edit_blog(blog_title):
    if request.method == "GET":
        blog = Post.query.filter_by(title=blog_title).first_or_404()
        form = BlogForm(title=blog.title, intro=blog.intro, content=blog.content, image=blog.image)
        return render_template("blog/edit_blog.html", form=form)
    

def save_blog_image(f ):
    filename = secure_filename(f.filename)
    BLOG_PHOTO_DIR = os.path.join(PROJECT_DIR, current_app.config["UPLOAD_FOLDER"])

    # create blog photo directory if it doesnt exist
    if not os.path.exists(BLOG_PHOTO_DIR):
        print("photo directory exists")
        os.makedirs(BLOG_PHOTO_DIR)
    
    # get full blog_path
    file_path = os.path.join(
        PROJECT_DIR, current_app.config["UPLOAD_FOLDER"], filename
    )
    f.save(file_path)

    return os.path.relpath(file_path, PROJECT_DIR)
