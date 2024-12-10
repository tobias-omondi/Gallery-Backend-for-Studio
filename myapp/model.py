from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps

db = SQLAlchemy()
bcrypt = Bcrypt()

# Images table
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(55), nullable=True)
    
    # Foreign key for reference to admin table
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_user.id'), nullable=True)

    # Relationship back to admin_user table
    admin_user = db.relationship('AdminUser', backref='images', lazy=True)

    def __init__(self, image_url, title):
        self.image_url = image_url
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "title": self.title
        }

# Videos table
class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Foreign key for reference to admin table
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_user.id'), nullable=True)

    # Relationship back to admin_user table
    admin_user = db.relationship('AdminUser', backref='videos', lazy=True)

    def __init__(self, video_url, title, description):
        self.video_url = video_url
        self.title = title
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "video_url": self.video_url,
            "title": self.title,
            "description": self.description
        }


# Admin User table
class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(70), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    def __init__(self, username , password, is_admin = True):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode("utf-8") # we are hashing the password
        self.is_admin = is_admin

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_admin": self.is_admin
        }
    # during login session to authenticate
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)
    
