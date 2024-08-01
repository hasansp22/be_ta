from app_py.model.KategoriModel import Kategori, db
from app_py import app, db, response
from flask import jsonify, request

def tampil_kategori():
    try:
        kategori = Kategori.query.all()
        result = []
        for i in kategori:
            result.append(
                {
                 'id': i.id,
                 'name': i.name_category,
                 }
            )
            
        return jsonify(result), 200
    
    except Exception as e:
        print(e)

def tampil_kategori_by_id(id):
    try:
        kategori = Kategori.query.get(id)
        if kategori:
            return jsonify({
                'id': kategori.id,
                'name': kategori.name_category,
            })
        
        else:
            return jsonify({'error': 'Kategori tidak ditemukan'})
    except Exception as e:
        print(e)


def simpan_kategori():
    try:
        data = request.get_json()
        name = data.get('name')

        kategori = Kategori(name_category = name)
        db.session.add(kategori)
        db.session.commit()

        return response.success('', 'Sukses menambah data')
        
    except Exception as e:
        print(e)

def edit_kategori(id):
    kategori = Kategori.query.get(id)
    if kategori:
        data = request.get_json()
        name = data.get('name')
        
        kategori.name = name
        db.session.commit()
        tampil_kategori()
            
        return response.success('', 'Sukses UPDATE data')

    else: 
        return jsonify({'message': 'kategori tidak ditemukan'})

def hapus_kategori(id):
    kategori = Kategori.query.get(id)
    if kategori:
        db.session.delete(kategori)
        db.session.commit()
        return jsonify({'message': 'Data kategori berhasil dihapus'})
    else:
        return jsonify({'message': 'Kategori tidak ditemukan'})
