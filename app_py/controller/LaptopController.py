from app_py.model.LaptopModel import Laptop, db
from app_py import app, db, response
from flask import jsonify, request

# def tampil_laptop():
#     try:
#         laptop = Laptop.query.all()
#         result = []
#         for i in laptop:
#             result.append(
#                 {
#                     'id': i.id,
#                     'name': i.name,
#                     'cpu': i.cpu,
#                     'gpu': i.gpu,
#                     'storage': i.storage,
#                     'ram': i.ram,
#                     'display': i.display,
#                 }
#             )
#     except Exception as e:
#         print(e)
