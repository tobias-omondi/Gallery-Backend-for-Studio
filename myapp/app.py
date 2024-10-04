from flask import Flask , request , jsonify
from flask_restful import Api ,Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from myapp.model import db , Image , Video , Podcast , Comment# Import db from models

app = Flask(__name__)

# Set up database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Studio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Flask-Migrate
db.init_app(app)  # Initialize db with app
migrate = Migrate(app, db)

api = Api(app)

# Define a HelloWorld resource
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

# api for images (crud) get, update, delete 

class imagesResource(Resource):
    def get(self):
        images = Image.query.all()
        return jsonify([image.to_dict() for image in images])
    
    def post(self):
        data = request.get_json()
        image_url = data.get('image_url')
        title = data.get('title')

        if not image_url or not title:
            return {"message": "Missing required fields: image_url, title"}, 400

        new_image = Image(image_url=image_url, title=title)
        try:
            db.session.add(new_image)
            db.session.commit()
            return {"message": "Image posted successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500

    def put(self):
        data = request.get_json()
        image_id = data.get('id')
        image_url = data.get('image_url')
        title = data.get('title')

        if not image_id:
            return {"message": "Missing required field: 'id'"}, 400

        image = Image.query.get(image_id)
        if not image:
            return {"message": "Image not found"}, 404

        if image_url:
            image.image_url = image_url
        if title:
            image.title = title

        try:
            db.session.commit()
            return {"message": "Image updated successfully", "image": image.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
        
    def delete(self):
        data = request.get_json()
        image_id = data.get('id')

        if not image_id:
            return {"message": "Missing required field: 'id'"}, 400

        image = Image.query.get(image_id)
        if not image:
            return {"message": "Image not found"}, 404

        try:
            db.session.delete(image)
            db.session.commit()
            return {"message": f"Image with id {image_id} deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500

api.add_resource(imagesResource, '/images')



# apis for videos ....
class VideosResources(Resource):
    def post(self):

        # used to request our data
        data = request.get_json()

        video_url = data.get('video_url')
        title = data.get('title')
        description = data.get('description')

        if not video_url or not title or not description:
            return {'message': "Missing fields required: video_url, title and description"}
        
        new_video =Video ( video_url= video_url , title = title , description = description)

        try:
            db.session.add(new_video)
            db.session.commit()
            return{'message': "Video successfuly posted"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"an error occured {str(e)} "}, 500
        
    def get(self):

        videos = Video.query.all() # get all videos information
        return jsonify ([video.to_dict() for video in videos])
    
    def put(self):
        data = request.get_json() #retrival of all videos data in json

        video_id = data.get('id')
        video_url = data.get('video_url')
        title = data.get('title')
        description = data.get('description')

        if not video_id:
            return {"message":"Missing required field:'id'"},400
        
        video = Video.query.get(video_id)
        if not video:
            return{"message": "video not found"},404
        
        if video_url:
            video.video_url = video_url
        if title:
            video.title = title
        if description:
            video.description = description

        try:
            db.session.commit()
            return {"message": "video updated successfully", "video": video.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
    

    def delete(self):

        data = request.get_json()
        Video_id = data.get('id')

        if not Video_id:
            return{"message": "Missing field invalid"},400
        
        video = Video.query.get(Video_id)
        if not video:
            return{"message": "video not found"},404
           
        
        try:
            db.session.delete(video)
            db.session.commit()
            return{"message": f"video with id {Video_id} deleted successfuly"},201
        except Exception as e:
            db.session.rollback()
            return {"message": f"an error occured {str(e)} "}, 500
        


api.add_resource(VideosResources, '/videos')


class PodcastResources(Resource):
    def post(self):

        # we are requestig the data from json
        data = request.get_json()

        audio_url = data.get('audio_url')
        title = data.get('title')
        description = data.get('description')

        if not audio_url or not title or not description:
            return{"message": "Missing invalid text ,'audio_url', 'title', 'description'"}
        
        new_podcast = Podcast(audio_url = audio_url , title = title , description = description)

        try:
            db.session.add(new_podcast)
            db.session.commit()
            return {"Message": "Podcast successfuly posted"},201
        except Exception as e:
            db.session.rollback()
            return {"Message": f"an error occured {str(e)}"},500
        
    def get(self):
        podcasts = Podcast.query.all()
        return jsonify ([podcast.to_dict() for podcast in podcasts])
    
    def put(self):

        data = request.get_json() # retrival of updates data

        audio_id = data.get('id')
        audio_url = data.get('audio_url')
        title = data.get('title')
        description = data.get('description')

        if not audio_id:
            return{"Message":"Missing field invalid"}, 404
        
        audio = Podcast.query.get(audio_id)
        if not audio:
            return{"message": "podcast not found"}
        
        if audio_url:
            audio.audio_url = audio_url
        if title:
            audio.title = title
        if description:
            audio.description = description

        try:
            db.session.commit()
            return {"message": "podcast updated successfully", "audio": audio.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
        
    def delete(self):

        data = request.get_json()
        audio_id =data.get('id')

        if not audio_id:
            return{"message": "Podcast does not exist"},404
        
        podcast_audio = Podcast.query.get(audio_id)
        if not podcast_audio:
            return {"Message": "podcast not found"}
        
        try:
            db.session.delete(podcast_audio)
            db.session.commit()
            return{"Message": f"podcast with id {audio_id} deleted successfuly"}, 203
        
        except Exception as e:
            db.session.rollbask()
            return {"Message": f" an error occured {str(e)}"}, 500

api.add_resource(PodcastResources , "/podcasts")


# comment apis

class CommentsResources(Resource):
    def post(self):
        data = request.get_json()
        message = data.get('message')
        posted_at = data.get('posted_at')
        admin_id = data.get('admin_id')
        notification_id = data.get('notification_id')

        if not message or not posted_at:
            return {"Message": "Message or posted date is missing"}, 400

        new_comment = Comment( message=message, posted_at=posted_at, admin_id=admin_id, notification_id=notification_id  )

        try:
            db.session.add(new_comment)
            db.session.commit()
            return {"Message": "Message successfully sent"}, 202
        except Exception as e:
            db.session.rollback()
            return {"Message": f"An error occurred: {str(e)}"}, 500

    def get(self):
        comments = Comment.query.all()
        return jsonify([comment.to_dict() for comment in comments])

    def delete(self):
        data = request.get_json()  # Requesting for comments message
        comment_id = data.get('id')

        if not comment_id:
            return {"Message": "Comment ID is required"}, 400

        comment = Comment.query.get(comment_id)

        if not comment:
            return {"Message": "Comment not found"}, 404

        try:
            db.session.delete(comment)
            db.session.commit()
            return {"Message": f"Comment {comment_id} successfully deleted"}, 203
        except Exception as e:
            db.session.rollback()
            return {"Message": f"An error occurred: {str(e)}"}, 502

api.add_resource(CommentsResources, "/comments")


class NotificationResources(Resource):

    def get(self):
        pass

    def post(self):
        pass
    def update(self):
        pass

    def delete(self):
        pass


api.add_resource(NotificationResources, '/notfication')


class AdminResources(Resource):

    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass
    def delete(self):
        pass

api.add_resource(AdminResources, '/admin')



# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
