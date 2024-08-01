from app_py import db
from datetime import datetime
from app_py.model.KategoriModel import *

class Kriteria(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
    name_kriteria = db.Column(db.String(100), nullable = False)
    # kategori_fk = db.Column(db.BigInteger, db.ForeignKey(Kategori.id), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow,)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Kriteria {}>'.format(self.name_kriteria)
