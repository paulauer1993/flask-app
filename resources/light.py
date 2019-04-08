from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_refresh_token_required, fresh_jwt_required

from main.models.light import LightModel

class Light(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("timestamp", type=str, required=True, help="This field cannot be left blank.")
    parser.add_argument("value", type=float, required=True, help="This field cannot be left blank.")

    @fresh_jwt_required
    def get(self, uid):
        light = LightModel.find_by_uid(uid)
        if light:
            return light.json()
        return {"message": "Light entry id not found."}, 404

    def delete(self, uid):
        light = LightModel.find_by_uid(uid)
        if light:
            light.delete_from_db()
            return {"message": f"Light entry with the uid {uid} deleted."}

        return {"message": f"No entry with the uid {uid}."}, 404


class AllLights(Resource):

    @fresh_jwt_required
    def get(self):
        return {"light": [light.json() for light in LightModel.query.all()]}  # list(map(lambda x: x.json(), ItemModel.query.all())}}

    @jwt_refresh_token_required
    def post(self):
        data = Light.parser.parse_args()
        light = LightModel(**data)  # data["price"], data["store_id"]

        try:
            light.save_to_db()
        except:
            return {"message": "Object uid already in use."}, 500

        return light.json(), 201
