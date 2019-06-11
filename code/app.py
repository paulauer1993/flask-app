import os

from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime

from models.user import UserModel
from models.temperature import TempModel
from models.humidity import HumidityModel
from models.light import LightModel

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

@app.route("/home", methods=["POST", "GET"])
def form_post():
    username = request.form["username"]
    password = request.form["password"]
    user = UserModel.find_by_username(username)

    if user and user.password == password:
        tmp = [temp["value"]  for temp in TempModel.query.all()]
        tmp = str(tmp[-1])
        hum = [hum["value"] for hum in HumidityModel.query.all()]
        hum = str(hum[-1])
        light = [light["value"] for light in LightModel.query.all()]
        light = str(light[-1])

        return render_template("home.html", temp_value=a, hum_value=hum_value, light_value=light_value), 200

    return render_template("login_failed.html"), 400


if __name__ == "__main__":
    from code.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
