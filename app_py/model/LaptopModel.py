from app_py import db
from datetime import datetime

class Laptop(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False)
    brand = db.Column(db.String(100), nullable = False)
    cpu = db.Column(db.String(100), nullable = False)
    gpu = db.Column(db.String(100), nullable = False)
    storage = db.Column(db.Integer, nullable = False)
    ram = db.Column(db.Integer, nullable = False)
    display = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Laptop {}>'.format(self.name)
