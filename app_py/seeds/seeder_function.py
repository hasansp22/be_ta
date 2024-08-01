from app_py.model.AdminModel import Admin
from app_py import db
from werkzeug.security import check_password_hash, generate_password_hash

def create_admins(num_admins):
    for _ in range(num_admins):
        username = "adm"
        password = generate_password_hash("adm12345")
        # check_password_hash(password)
        admin = Admin(name = username, password = password)
        db.session.add(admin)
    db.session.commit()