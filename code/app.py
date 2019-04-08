from flask import Flask
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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = False

app.secret_key = "b'_5#y2LF4Q8z%nx*ec]/"
api = Api(app)

jwt = JWTManager(app)

api.add_resource(AllTemps, "/temperature")
api.add_resource(Temperature, "/temperature/<int:uid>")
api.add_resource(AllHumidity, "/humidity")
api.add_resource(Humidity, "/humidity/<int:uid>")
api.add_resource(AllLights, "/light")
api.add_resource(Light, "/light/<int:uid>")

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    from code.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

