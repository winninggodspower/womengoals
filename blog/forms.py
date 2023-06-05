from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_ckeditor import CKEditorField

class BlogForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    # slug
    content = CKEditorField('content')
    image = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

    submit = SubmitField('submit')