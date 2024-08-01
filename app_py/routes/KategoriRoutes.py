from app_py import app
from app_py.controller.KategoriController import *

@app.route('/')
def index():
  return 'hello'

@app.route('/kategori', methods = ['GET'])
def kategoris():
  return tampil_kategori()

@app.route('/kategori/<int:id>', methods = ['GET'])
def kategoris_by_id(id):
  return tampil_kategori_by_id(id)

@app.route('/kategori/simpan', methods = ['POST'])
def kategoris_save():
  return simpan_kategori()

@app.route('/kategori/edit/<int:id>', methods = ['PUT'])
def kategoris_edit(id):
  return edit_kategori(id)

@app.route('/kategori/hapus/<int:id>', methods = ['DELETE'])
def kategoris_delete(id):
  return hapus_kategori(id)