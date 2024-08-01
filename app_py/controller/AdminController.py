from app_py.model.AdminModel import Admin
from app_py import app, db, response
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask import jsonify, request, session, redirect, url_for
from flask_jwt_extended import *
import datetime

jwt = JWTManager(app)

# def login():
#     try:
#         data = request.get_json()
    
#         user = data.get('username')
#         pw = data.get('password')

#         admin = Admin.query.filter_by(username = user).first()

#         if admin is None:
#             return jsonify({'error' : 'Admin not found'}), 401
        
#         if not check_password_hash(admin.password, pw):
#             return jsonify({'error' : 'Password incorrect'}), 401
        
#         session['admin_id'] = admin.id
#         session['username_id'] = admin.username

#         id = session.get('admin_id')
#         name = session.get('username_id')
        
#         return jsonify({
#             'id' : admin.id,
#             'username' : admin.username,
#         })
    
#         # return response.success('', 'berhasil login')
        
#     except Exception as e:
#         print(e)


def signup():
    data = request.get_json()
    
    user = data.get('username')
    pw = data.get('password')
    hash_pass = generate_password_hash(pw)

    check_admin = Admin.query.filter_by(username = user).first() is not None

    if check_admin:
        return jsonify({'error' : 'Admin exist!'}), 409

    new_admin = Admin(username = user, password = hash_pass)

    db.session.add(new_admin)
    db.session.commit()

    session['admin_id'] = new_admin.id

    # return response.success('', 'sukses')
    return jsonify({
        "id" : new_admin.id,
        "username" : new_admin.username
    })

def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('login'))
        return route_function(*args, **kwargs)
    return decorated_function

def logins():
    data = request.get_json()
    user = data.get('username')
    pw = data.get('password')

    admin = Admin.query.filter_by(username = user).first()

    if admin is None:
        return jsonify({'error' : 'Admin not found'}), 401
            
    if not check_password_hash(admin.password, pw):
        return jsonify({'error' : 'Password incorrect'}), 401
        
    session['admin_id'] = admin.id

    expires = datetime.timedelta(days = 7)
    expires_refersh = datetime.timedelta(days = 7)

    access_token = create_access_token(admin.id, fresh = True, expires_delta = expires)
    refresh_token = create_refresh_token(admin.id, expires_delta = expires_refersh)

    return jsonify({
        'message': 'Login berhasil',
        'access_token' : access_token,
        'refresh_token' : refresh_token,
        'session_admin' : session.get('admin_id')
    })

@login_required
# @jwt_required()
def profile():
    admin_id = session.get('admin_id')
    # username = session.get('username')
    admin = Admin.query.get(admin_id)

    # current_user = get_jwt_identity()

    if not admin:
        return jsonify({'error' : 'Admin not found!'})
    
    return jsonify({
        'admin_id' : admin.id,
        'username' : admin.username
    })

@login_required
# @jwt_required()
def logout():
    # session.pop('admin_id', None)
    session.clear()
    # jti = get_raw_jwt()['jti']
    return jsonify({'message': 'Logout berhasil'})