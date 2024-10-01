from App import db


# Images table
class images(db.Model):
    __tablename = 'Images'
    id = db.Column(db.Interger, primary_KEY=True)
    image_url = db.Column(db.text, nullable = False )
    title = db.Column(db.String(55), nullable = True)

    # relationship
    admin_id = db.Column(db.String(55), nullable = False)

class videos(db.Model):
    __tablename__ = 'Videos'
    id = db.Column(db.Interger, primary_key =True)
    video_url = db.Column(db.String(500), nullable = False)
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text, nullable = False)

    # creat a relationship
    admin_id = db.Column(db.String(55), nullable = False)

class podcast(db.Model):
    __tablename__ = "Podcast"
    id = db.Column(db.Interger, primary_key = True)
    audio_url = db.Column(db.String(255), nullable = True)
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text, nullable = False)

       # creat a relationship
    admin_id = db.Column(db.String(55), nullable = False)

class comments (db.Model):
    __tablename__ = "Comments"
    id = db.Column(db.Interger, primary_key = True)
    message = db.Column(db.Text, nullable = False)
    posted_at = db.Column(db.Text, nullable = False)

       # creat a relationship
    admin_id = db.Column(db.String(55), nullable = False)

class notfications (db.Model):
    __tablename__ = "Notifications"

    id = db.Column(db.Interger, primary_key = True)
    