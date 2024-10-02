from flask import Flask , request , jsonify
from flask_restful import Api ,Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from myapp.model import db , Image # Import db from models

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

class ImagesResource(Resource):

    def post(self):
        data = request.get_json()

        image_url =data.get('image_url')
        title = data.get('title')

        if not image_url or not title:
            return{"message": "Missing required Fields:image_url"}, 400
        new_image = Image(image_url=image_url, title=title)

        try:
            db.session.add(new_image)
            db.session.commit()
            return{"message" :"Image posted Successfuly"}, 201
        except Exception as e:
            db.session.rollback()
            return{"message" : f"An error occured: {str(e)}"}, 500


    def get(self):
        images = Image.query.all() #we are fetching all the images records
        return jsonify([image.to_dict() for image in images]) 

api.add_resource(ImagesResource, '/images')

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
