
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registrarse", methods=["POST"])
def registrarse():
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    telefono = data.get("telefono")
    password = data.get("password")
    hashed_pw = generate_password_hash(password)
    # insertar usuario con hashed_pw
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO usuarios 
             (nombre,apellido, email, telefono, password) 
             VALUES (%s, %s, %s, %s, %s)"""
    values = (nombre,apellido, email, telefono,hashed_pw)
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"message": "registro exitoso"}

@auth_bp.route("/login", methods=["POST"])
def login():
    # buscar user
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = User.get_by_email(email)
    if user and check_password_hash(user.password, password):
        login_user(user)
        return {"message": "Login exitoso"}
    return {"message": "Datos errados"}

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()