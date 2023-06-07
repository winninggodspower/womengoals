from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from .auth import auth
from .forms import BlogForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import os
from .models import Post, db
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileAllowed


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
blog = Blueprint('blog', __name__, url_prefix='/blog')

class BlogConfig:
    def __init__(self, app) -> None:
        app.config["UPLOAD_FOLDER"] = os.getenv('UPLOAD_FOLDER')
        app.config["UPLOAD_SUB_FOLDER"] = os.getenv('UPLOAD_SUB_FOLDER')
        ckeditor = CKEditor(app)
        csrf = CSRFProtect(app)



@blog.route("/", methods=['GET', 'POST'])
def view_all_blog():
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


@blog.route("/edit_blog/<string:blog_id>", methods=["GET", "POST"])
@auth.login_required
def edit_blog(blog_id):
    form = BlogForm()
    # Remove DataRequired validator for image field in the edit route
    form.image.validators = [FileAllowed(['jpg', 'png'], 'Images only!')]
    
    blog = Post.query.filter_by(id=blog_id).first_or_404()

    if form.validate_on_submit():
        image_path = save_blog_image(form.image.data) # save blog image

        # Update the post with the new data
        blog.title = form.title.data
        blog.intro = form.intro.data
        blog.content = form.content.data
        blog.image = image_path

        # Save the changes to the database
        db.session.commit()

        flash('Blog has been updated successfully.', 'success')
        return redirect(url_for('blog.view_blog', blog_slug=blog.slug))

    form = BlogForm(title=blog.title, intro=blog.intro, content=blog.content, image=blog.image)
    return render_template("blog/edit_blog.html", form=form, blog=blog)
    

@blog.route("/delete_blog/<string:blog_id>", methods=["GET"])
def delete_blog(blog_id):
    blog = Post.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash("succesfully deleted blog post", "success")
    return redirect(url_for('blog.view_all_blog'))
    

def save_blog_image(f ):
    filename = secure_filename(f.filename)
    BLOG_PHOTO_DIR = os.path.join(PROJECT_DIR, current_app.config["UPLOAD_FOLDER"], current_app.config["UPLOAD_SUB_FOLDER"])

    # create blog photo directory if it doesnt exist
    if not os.path.exists(BLOG_PHOTO_DIR):
        os.makedirs(BLOG_PHOTO_DIR)
    
    # get full blog_path
    file_path = os.path.join(
        BLOG_PHOTO_DIR, filename
    )
    f.save(file_path)

    return f"/{current_app.config['UPLOAD_SUB_FOLDER']}/{filename}"
