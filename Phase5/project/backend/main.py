import os
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import flask_restful
from flask import Flask
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
           



@app.shell_context_processor
def make_shell_context():
    return{
        "db":db,
        "User":User,
        "Event":Event
    }


if __name__ == "__main__":
    app.run()