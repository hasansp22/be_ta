from app_py import app
from app_py.controller.KriteriaController import *


@app.route('/kriteria', methods=['GET'])
def kriterias_tampil():
    return tampil_kriteria()

@app.route('/kriteria/<int:id>', methods=['GET'])
def kriterias_by_id(id):
    return tampil_kriteria_by_id(id)

@app.route('/kriteria/simpan', methods=['POST'])
def kriterias_save():
    return simpan_kriteria()

@app.route('/kriteria/edit/<int:id>', methods=['PUT'])
def kriterias_edit(id):
    return edit_kriteria(id)

@app.route('/kriteria/hapus/<int:id>', methods=['DELETE'])
def kriterias_delete(id):
    return hapus_kriteria(id)

@app.route('/kriteria/hitung', methods=['POST'])
def kriterias_hitung():
    return hitung_kriteria()

@app.route("/tampil")
def tampils():
    return tampil()
    # return None

@app.route('/kriteria/filter', methods=['POST'])
def filter_laptops():
    return filter_laptop()
    # return None
