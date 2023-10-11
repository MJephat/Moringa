import os
from flask import Flask,request,jsonify, render_template,make_response
from flask_restx import Api, Resource,fields
from config import DevConfig
from exts import db
from flask_cors import CORS
from model import User, Event
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager,get_jwt_identity, create_access_token, create_refresh_token, jwt_required
from werkzeug import *
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from cloudinary.uploader import upload
# from mailjet import Mailjet
from mailjet_rest import Client

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config.from_object(DevConfig)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

migrate = Migrate(app, db)
JWTManager(app)

api = Api(app, doc="/docs")


# Configuring Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

config = cloudinary.config(secure=True)


# model serializer
event_model = api.model(
    "Event",
    {
        "id": fields.Integer(),
        "host": fields.String(),
        "title": fields.String(),
        "media": fields.String(),
        "location": fields.String(),
        "time": fields.String(),
        "date": fields.String(),
        "price": fields.String()
    },
)

signup_model = api.model(
    "SignUp",
    {
        "userName":fields.String(),
        "email":fields.String(),
        "password":fields.String(),

    }
)

login_model = api.model(
    "Login",
    {
        "userName":fields.String(),
        "password":fields.String(),

    }
)

@api.route("/signup", methods=["POST"])
class Signup(Resource):
    @api.expect(signup_model)
    def post(self):
        # Get the user data from the request's JSON body
        data = request.get_json()
        # Create a new User object with the provided data
        userName = data.get('userName')
        db_user = User.query.filter_by(userName=userName).first()

        if db_user is not None:
            return jsonify({"message":f"User with username {userName} already exists"})
        
        new_user = User(
            userName=data.get("userName"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password"))
        )

            # Add the new_user to the database and commit the changes
        db.session.add(new_user)
        db.session.commit()
        # new_user.save()
        return make_response(jsonify({"message":"user created successiful"}),201)
        

    @api.route("/login", methods=["POST"])
    class Login(Resource):
        @api.expect(login_model)
        def post(self):
            data = request.get_json()

            userName = data.get("userName")
            password = data.get("password")


            db_user=User.query.filter_by(userName=userName).first()

            if db_user and  check_password_hash(db_user.password, password):
            
                access_token=create_access_token(identity=db_user.userName, fresh=True)
                refresh_token=create_refresh_token(identity=db_user.userName)
                
                return jsonify(
                    {"access_token":access_token, "refresh_token":refresh_token}
                )
                pass

# http methods on event.
@api.route("/events", methods=['GET'])
class EventsList(Resource):
    @api.marshal_list_with(event_model)
    def get(self):
        """Get all reports"""
        events = Event.query.all()
        return events  


@api.route("/upload", methods=['POST'])
class Upload(Resource):
    @api.expect(event_model)
    def post(self):
        if request.method == "POST":
            file_to_upload = request.files["file"]
            if file_to_upload or file_to_upload.filename == "":
                upload_result = cloudinary.uploader.upload(file_to_upload)
                price = request.form.get('price')
                host = request.form.get("host")
                title = request.form.get('title')
                location = request.form.get('location')
                time = request.form.get('time')
                date = request.form.get('date')
               
                event = Event(
                        price=price,
                        host=host,
                        title=title,
                        media=upload_result["url"],
                        location=location,
                        time=time,
                        date=date,
                    )
                db.session.add(event)
                db.session.commit()
                return make_response(jsonify({"message": "Media and event uploaded successfully"}), 201)
            else:
                    return jsonify({"error": "file not found."}), 404




@api.route('/event/<int:id>')
class EventResource(Resource):
    @api.marshal_with(event_model)
    def get(self,id):
        """get a report by id"""
        event=Event.query.get_or_404(id)

        return event
        pass

@app.route("/events/<int:event_id>", methods=['DELETE'])
def delete_event(report_id):
        # Get the report by ID
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found.'}), 404
        # Delete the report from the database
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully.'}) 


@app.route("/events/<int:event_id>", methods=['PATCH'])
def update_event(event_id):
    # Get the event by ID
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found.'}), 404
    # Get the updated data from the request
    data = request.json
    # Update the event fields with the new data
    event.host= data.get('host', event.host)
    event.title = data.get('title', event.title)
    event.location = data.get('location', event.location)
    event.time = data.get('time', event.time)
    event.date = data.get('date', event.date)
    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Report updated successfully.'})


@app.route("/events/<int:event_id>/media", methods=['PATCH'])
def update_event_media(event_id):
    # Get the event by ID
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found.'}), 404
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided.'}), 400
    file_to_upload = request.files['file']
    if file_to_upload:
        # Upload the image to Cloudinary
        upload_result = cloudinary.uploader.upload(file_to_upload)
        app.logger.info(upload_result)
        # Update the report media URL in the database
        event.media = upload_result['url']
        db.session.commit()
        return jsonify({'message': 'Event updated successfully.'})


@app.shell_context_processor
def make_shell_context():
    return{
        "db":db,
        "User":User,
        "Event":Event
    }


if __name__ == "__main__":
    app.run()