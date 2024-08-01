from app_py import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class Admin(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(250), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow,)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Admin {}>'.format(self.username, self.password)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.pass_admin, password)
    
    
