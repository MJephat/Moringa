import os
from flask import Flask,request,jsonify, render_template,make_response
from flask_restx import Api, Resource,fields
from config import DevConfig
from exts import db
from flask_cors import CORS
from model import User
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager,get_jwt_identity, create_access_token, create_refresh_token, jwt_required
from werkzeug import *
from flask_sqlalchemy import SQLAlchemy
from flask.globals import app_ctx
from flask.appctx import app_ctx


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config.from_object(DevConfig)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

migrate = Migrate(app, db)
# JWTManager(app)

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

@app.route("/signup", methods=["POST"])
def signup():
    # Get the user data from the request's JSON body
    data = request.json
    # Create a new User object with the provided data
    new_user = User(
        userName=data["userName"],
        email=data["email"],
        password=data["password"],
    )

        # Add the new_user to the database and commit the changes
    db.session.add(new_user)
    db.session.commit()

    @api.route("/login", methods=["POST"])
    class Login(Resource):
        @api.expect(login_model)
        def post(self):
            data = request.get_json()

            userName = data.get("userName")
            password = data.get("password")

            user = User.query.filter_by(userName=userName).first()

            if user and  check_password_hash(user.password, password):
            
                access_token=create_access_token(identity=user.userName, fresh=True)
                refresh_token=create_refresh_token(identity=user.userName)
                
                return jsonify(
                    {"access_token":access_token, "refresh_token":refresh_token}
                )


@app.shell_context_processor
def make_shell_context():
    return{
        "db":db,
        "events":events,
        "User":User,
    }


if __name__ == "__main__":
    app.run()