# Gallery-Backend-for-Studio

## Overview
The studio app is built with restful api using flask and SQLAlchemy.This application serves as a backend for managing various resource in a related galler studio. it will include notification,images,videos,admin panel,podcast and comments from user but there will be no user authentication. The app is design to showcase clients the work of a studio business.

## Features
* Images management - Delete,Update,Create and Post
* Videos management - Delete,Update,Create and Post
* Podcast management - Delete,Update,Create and Post
* Comments management - Delete,Update,Create and Post
* notification management - Delete,Update,Create and Post

## Tech Used.
* Flask: A lightweight WSGI web application framework.
* Flask SQLAlchemy:An ORM (Object Relational Mapper) for database interactions.
* Flask Admin: For admin panel
  ` Flask Login: admin creditionals & admin session managment
- Flask- Restful: manage Apis
- Flask- Bycrypt:for password hashing

## Installation
    git clone git@github.com:tobias-omondi/Gallery-Backend-for-Studio.git
    cd Gallery-Backend-for-Studio/
### set up vertual Enviroment
    python3 -m venv venv
    source venv/bin/activate  
    export FLASK_APP=myapp.app

### install Dependencies:
    pip install -r  requirements.txt
### set up database
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade
### run application
    flask run

# API END POINTS
### Images
* POST /api/images: Add a new image.
* GET /api/images: Get a list of all images.
* PUT /api/images/<id>: Update an existing image.
* DELETE /api/images/<id>: Delete an image.
#### Videos
* POST /api/videos: Add a new video.
* GET /api/videos: Get a list of all videos.
* PUT /api/videos/<id>: Update an existing video.
* DELETE /api/videos/<id>: Delete a video.
### Podcasts
* POST /api/podcasts: Add a new podcast.
* GET /api/podcasts: Get a list of all podcasts.
* PUT /api/podcasts/<id>: Update an existing podcast.
* DELETE /api/podcasts/<id>: Delete a podcast.
### Comments
* POST /api/comments: Add a new comment.
* GET /api/comments: Get a list of all comments.
* PUT /api/comments/<id>: Update an existing comment.
* DELETE /api/comments/<id>: Delete a comment.
### Notifications
* POST /api/notifications: Add a new notification.
* GET /api/notifications: Get a list of all notifications.
* PUT /api/notifications/<id>: Update an existing notification.
* DELETE /api/notifications/<id>: Delete a notification.
### Admin
