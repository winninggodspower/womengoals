from flask_sqlalchemy import SQLAlchemy
from unicodedata import normalize
from datetime import datetime

db = SQLAlchemy()

class DbConfig:
    def __init__(self, app):
        # configure the SQLite database, relative to the app instance folder
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug  = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))  # Change the size as per your needs
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = self.slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)

    def slugify(self, text, encoding=None,
        permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):

        clean_text = text.strip().replace(' ', '-').lower()
        while '--' in clean_text:
            clean_text = clean_text.replace('--', '-')
        ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
        strict_text = map(lambda x: str(x) if str(x) in permitted_chars else '', ascii_text)
        return ''.join(strict_text)
    
    
