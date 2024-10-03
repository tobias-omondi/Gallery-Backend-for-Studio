from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    def __init__(self,video_url, title, description):
        self.video_url = video_url
        self.title = title
        self.description = description

    def to_dict(self):
        return{
            "id":self.id,
            "video_url": self.video_url,
            "title":self.title,
            "description": self.description
        }
# Podcast table
class Podcast(db.Model):
    __tablename__ = 'podcasts'
    id = db.Column(db.Integer, primary_key=True)
    audio_url = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Foreign key for reference to admin table
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_user.id'), nullable=True)

    # Relationship back to admin_user table
    admin_user = db.relationship('AdminUser', backref='podcasts', lazy=True)


# Comments table
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.String(255), nullable=False) 
    
    # Foreign key for reference to notification table and admin table
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_user.id'), nullable=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=True)

    # Relationships back to AdminUser and Notification tables
    admin_user = db.relationship('AdminUser', backref='comments', lazy=True)
    notification = db.relationship('Notification', backref='comments_list', lazy=True)  


# Notification table
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships back to Comment and AdminUser tables
    comments = db.relationship('Comment', backref='notification_popup', lazy=True)


# Admin User table
class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    
    # Foreign key reference to notifications table
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=True)

    # Relationship back to Notification table
    notification = db.relationship('Notification', backref='admin_users', lazy=True)
