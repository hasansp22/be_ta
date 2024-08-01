from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from flask_seeder import Seeder, FlaskSeeder
from faker import Faker, generator
from app_py import app, db
from app_py.model.AdminModel import Admin
from app_py.seeds.seeder_function import create_admins

seeds = FlaskSeeder(app)
seeds.init_app(app, db)


# @app.cli.command()
# def seed():
#     with app.app_context():
#         db.create_all()
#         create_admins(1)  # Ubah jumlah admin sesuai kebutuhan Anda
#         seeds.run()
#     print('Seeder executed successfully!')

# All seeders inherit from Seeder
class AdminSeeder(Seeder):
#   run() will be called by Flask-Seeder
    def run(self):
        password = generate_password_hash("adm12345")
        check_password_hash(password)
    # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls = Admin,
            init = {
                "id": '',
                "username": "adm",
                "password": password
            }
        )

        # Create admin
        for admin in faker.create(1):
            print("Adding : %s" % admin)
            self.db.session.add(admin)
