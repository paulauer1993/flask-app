from code.db import db

class HumidityModel(db.Model):
    __tablename__ = "humidity"

    uid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(80))
    value = db.Column(db.Float(precision=4))

    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def json(self):
        return {"uid": self.uid, "timestamp": self.timestamp, "value": self.value}

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).first()    # SELECT * FROM items WHERE name=name, limit=1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        return cls.query.order_by().all()