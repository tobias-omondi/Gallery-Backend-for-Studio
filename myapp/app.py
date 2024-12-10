from flask import Flask , request , jsonify
from flask_restful import Api ,Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from myapp.model import db , Image , Video , AdminUser# Import db from models
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity , jwt_required ,  JWTManager
import os
from functools import wraps



app = Flask(__name__)
CORS(app)
# Initialize Bcrypt
bcrypt = Bcrypt()


# Set up database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Studio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins=["https://studio-app-nine.vercel.app/"])
# intializing Jwt
app.config ['JWT_SECRET_KEY'] = os.getenv ("my_secret_key")
jwt = JWTManager(app)
db.init_app(app) 
migrate = Migrate(app, db)

api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')



# A decorator to check if the current user is an admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        # Check if the user is an admin (this assumes the `is_admin` field exists in the AdminUser model)
        admin = AdminUser.query.filter_by(username=current_user).first()
        if not admin or not admin.is_admin:
            return {"message": "Permission denied. Admins only."}, 403
        return fn(*args, **kwargs)
    return wrapper

# Example: Protecting the POST, PUT, and DELETE methods
class ImagesResource(Resource):
    @jwt_required()
    @admin_required
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

    @jwt_required()
    @admin_required
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

    @jwt_required()
    @admin_required
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


# api for images (crud) get, update, delete 

class imagesResource(Resource):
    def get(self):
        images = Image.query.all()
        return jsonify([image.to_dict() for image in images])
    
    @jwt_required()
    @admin_required
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
        
    @jwt_required()
    @admin_required
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
        

    @jwt_required()
    @admin_required    
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


    @jwt_required()
    @admin_required
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
    

    @jwt_required()
    @admin_required
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
    
    @jwt_required()
    @admin_required
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


class AdminResources(Resource):
    # @jwt_required()
    # @admin_required
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin', True)

        if not username or not password:
            return {"Message": "Missing required fields"}, 400

        # Check if the username already exists
        existing_user = AdminUser.query.filter_by(username=username).first()
        if existing_user:
            return {"Message": "Username already exists"}, 400
        
        # Hash password before creating the user
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        admin_user = AdminUser(username=username, password=hashed_password, is_admin=is_admin)

        try:
            db.session.add(admin_user)
            db.session.commit()
            return {"Message": "Admin created successfully"}, 201
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error occurred: {str(e)}")  # Log the error for debugging
            return {"Message": f"An error occurred: {str(e)}"}, 500

    def get(self):
        admin_users = AdminUser.query.all()
        return jsonify([admin_user.to_dict() for admin_user in admin_users])

    @jwt_required()
    @admin_required
    def put(self):
        data = request.get_json()
        
        admin_user_id = data.get('id')
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin')

        if not admin_user_id:
            return {"Message": "Missing required field: 'id'"}, 400
        
        admin_user = AdminUser.query.get(admin_user_id)
        if not admin_user:
            return {"Message": "Admin not found"}, 404
        
        if username:
            admin_user.username = username
        if password:
            admin_user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        if is_admin is not None:  # Check for None to allow updates
            admin_user.is_admin = is_admin

        try:
            db.session.commit()
            return {"Message": "Admin updated successfully"}, 200
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return {"Message": f"An error occurred: {str(e)}"}, 500

    @jwt_required()
    @admin_required
    def delete(self):
        data = request.get_json()
        admin_user_id = data.get('id')
        
        if not admin_user_id:
            return {"Message": "Missing required field: 'id'"}, 400
            
        admin_user = AdminUser.query.get(admin_user_id)
        
        if not admin_user:
            return {"Message": "Admin user not found"}, 404 
        
        try:
            db.session.delete(admin_user)  # Delete the user
            db.session.commit()
            return {"Message": f"Admin user with id {admin_user_id} deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return {"Message": f"An error occurred: {str(e)}"}, 500

api.add_resource(AdminResources, '/admin')

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"Message": "Missing username or password"}, 400

        print(f"Attempting login for username: {username}")

        # Query the user by username
        admin_user = AdminUser.query.filter_by(username=username).first()

        if admin_user is None:
            print("User not found")
            return {"Message": "Invalid Credentials"}, 401

        print(f"Stored Hashed Password: {admin_user.password}")
        print(f"Provided Password: {password}")

        if bcrypt.check_password_hash(admin_user.password, password):
            access_token = create_access_token(identity=username)
            return {"Message": "Login successful", "access_token": access_token}, 200
        
        print("Invalid password")
        return {"Message": "Invalid Credentials"}, 401
    
# Add resource to API
api.add_resource(LoginResource, '/login')



# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
