from flask import Blueprint, request, jsonify
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios", methods=["GET"])
@login_required
def get_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(usuarios)

@usuarios_bp.route("/usuario/<int:id>", methods=["GET"])
@login_required
def get_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from usuarios where idusuario=%s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(usuario)

@usuarios_bp.route("/usuarios", methods=["POST"])
@login_required
def add_usuario():
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    telefono = data.get("telefono")
    password = data.get("password")
    hashed_pw = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO usuarios 
             (nombre,apellido, email, telefono,password) 
             VALUES (%s, %s, %s, %s, %s)"""
    values = (nombre,apellido, email, telefono, hashed_pw)
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message":"usuario agregado"})

@usuarios_bp.route("/usuarios/<int:id>", methods=["PUT"])
@login_required
def update_usuario(id):
    data = request.json
    email = data.get("email")
    telefono = data.get("telefono")
    conn = get_db_connection()
    cursor = conn.cursor()
    values = (email,telefono, id)
    cursor.execute("update usuarios set email=%s, telefono=%s where idusuario=%s", values)
    conn.commit()
    cursor.close()
    conn.close
    return jsonify({"message":"usuario actualizado"})

@usuarios_bp.route("/usuarios/<int:id>", methods=["DELETE"])
@login_required
def delete_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    values = (id,)
    cursor.execute("delete from usuarios where idusuario=%s", values)
    conn.commit()
    cursor.close()
    conn.close
    return jsonify({"message":"usuario eliminado"})


