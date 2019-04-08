from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_refresh_token_required, fresh_jwt_required

from models.temperature import TempModel

class Temperature(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("timestamp", type=str, required=True, help="This field cannot be left blank.")
    parser.add_argument("value", type=float, required=True, help="This field cannot be left blank.")

    @fresh_jwt_required
    def get(self, uid):
        temp = TempModel.find_by_uid(uid)
        if temp:
            return temp.json()
        return {"message": "Temperature id not found."}, 404

    def delete(self, uid):
        temp = TempModel.find_by_uid(uid)
        if temp:
            temp.delete_from_db()
            return {"message": f"Temperature with the id {uid} deleted."}

        return {"message": f"No entry with the uid {uid}."}, 404


class AllTemps(Resource):

    @fresh_jwt_required
    def get(self):
        return {"temperatures": [temp.json() for temp in TempModel.query.all()]}    #list(map(lambda x: x.json(), ItemModel.query.all())}}

    @jwt_refresh_token_required
    def post(self):
        data = Temperature.parser.parse_args()
        temp = TempModel(**data)          #data["price"], data["store_id"]

        try:
            temp.save_to_db()
        except:
            return {"message": "Object uid already in use."}, 500

        return temp.json(), 201
