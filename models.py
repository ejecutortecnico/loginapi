from flask_login import UserMixin
from db import get_db_connection

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    @staticmethod
    def get_by_email(email):
        # consulta a la tabla usuarios
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from usuarios where email=%s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    @staticmethod
    def get_by_id(user_id):
        # consulta por id
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from usuarios where id=%s", (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario