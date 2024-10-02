from flask import Flask
from flask_restful import Api ,Resource
from flask_migrate import Migrate
from myapp.model import db  # Import db from models

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
