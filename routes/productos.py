from flask import Blueprint, request, jsonify
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/productos", methods=["GET"])
#@login_required
def get_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(productos)

@productos_bp.route("/producto/<int:id>", methods=["GET"])
#@login_required
def get_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from productos where idproducto=%s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(producto)

@productos_bp.route("/productos", methods=["POST"])
#@login_required
def add_producto():
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    telefono = data.get("telefono")
    password = data.get("password")
    hashed_pw = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO productos 
             (nombre,apellido, email, telefono,password) 
             VALUES (%s, %s, %s, %s, %s)"""
    values = (nombre,apellido, email, telefono, hashed_pw)
    cursor.execute(sql, values)
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message":"producto agregado"})

@productos_bp.route("/productos/<int:id>", methods=["PUT"])
#@login_required
def update_producto(id):
    data = request.json
    email = data.get("email")
    telefono = data.get("telefono")
    conn = get_db_connection()
    cursor = conn.cursor()
    values = (email,telefono, id)
    cursor.execute("update productos set email=%s, telefono=%s where idproducto=%s", values)
    conn.commit()
    cursor.close()
    conn.close
    return jsonify({"message":"producto actualizado"})

@productos_bp.route("/productos/<int:id>", methods=["DELETE"])
#@login_required
def delete_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    values = (id,)
    cursor.execute("delete from prodcutos where id=%s", values)
    conn.commit()
    cursor.close()
    conn.close
    return jsonify({"message":"producto eliminado"})


