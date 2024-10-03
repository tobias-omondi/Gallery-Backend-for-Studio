from flask import Flask , request , jsonify
from flask_restful import Api ,Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from myapp.model import db , Image , Video # Import db from models

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
    
api.add_resource(VideosResources, '/videos')



# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
