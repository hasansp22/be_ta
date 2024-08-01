from app_py import db
from datetime import datetime

class Kategori(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
    name_category = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow,)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Kategori {}>'.format(self.name)
