from app_py import app
from app_py.controller.AdminController import *
from functools import wraps
# from flask import Flask, session, redirect, url_for, request, jsonify

@app.route('/signup', methods = ['POST'])
def signup_():
  return signup()

# @app.route('/login', methods = ['POST'])
# def login_():
#   return login()

@app.route('/logins', methods=['POST'])
def logins_():
    return logins()

@app.route('/profile', methods=['GET'])
@login_required
def profile_():
    return profile()

@app.route('/logout', methods=['POST'])
@login_required
def logout_():
    return logout()