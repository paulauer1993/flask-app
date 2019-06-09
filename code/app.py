import os

from models.user import UserModel
from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime

from resources.user import UserRegister, UserLogin
from resources.temperature import Temperature, AllTemps
from resources.humidity import Humidity, AllHumidity
from resources.light import Light, AllLights

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["1000/hour"])

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = False

app.secret_key = "b'_5#y2LF4Q8z%nx*ec]/"
api = Api(app)

jwt = JWTManager(app)

api.add_resource(AllTemps, "/api/temperature")
api.add_resource(Temperature, "/api/temperature/<int:uid>")
api.add_resource(AllHumidity, "/api/humidity")
api.add_resource(Humidity, "/api/humidity/<int:uid>")
api.add_resource(AllLights, "/api/light")
api.add_resource(Light, "/api/light/<int:uid>")

api.add_resource(UserRegister, "/api/register")
api.add_resource(UserLogin, "/api/login")

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def form_post():
    username = request.form["username"]
    password = request.form["password"]
    user = UserModel.find_by_username(username)

    if user and user.password == password:
        return render_template("#"), 200

    return render_template("login_failed.html"), 400


if __name__ == "__main__":
    from code.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
