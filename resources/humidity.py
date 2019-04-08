from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_refresh_token_required, fresh_jwt_required

from models.humidity import HumidityModel

class Humidity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("timestamp", type=str, required=True, help="This field cannot be left blank.")
    parser.add_argument("value", type=float, required=True, help="This field cannot be left blank.")

    @fresh_jwt_required
    def get(self, uid):
        hum = HumidityModel.find_by_uid(uid)
        if hum:
            return hum.json()
        return {"message": "Humidity id not found."}, 404

    def delete(self, uid):
        hum = HumidityModel.find_by_uid(uid)
        if hum:
            hum.delete_from_db()
            return {"message": f"Humidity with the id {uid} deleted."}

        return {"message": f"No entry with the uid {uid}."}, 404


class AllHumidity(Resource):
    @fresh_jwt_required
    def get(self):
        return {"humidity": [hum.json() for hum in HumidityModel.query.all()]}  # list(map(lambda x: x.json(), ItemModel.query.all())}}

    @jwt_refresh_token_required
    def post(self):
        data = Humidity.parser.parse_args()
        hum = HumidityModel(**data)  # data["price"], data["store_id"]

        try:
            hum.save_to_db()
        except:
            return {"message": "Object uid already in use."}, 500

        return hum.json(), 201
