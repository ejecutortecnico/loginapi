from flask import Flask
from flask_login import LoginManager
from models import User
from routes.login import auth_bp
from routes.usuarios import usuarios_bp
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = "clave_secreta"

login_manager = LoginManager(); 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/")
def home():
    return "hola flask"

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(usuarios_bp, url_prefix="/api")
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": ["http://127.0.0.1:5173", "http://localhost:5173"]
    }
})

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,  # True solo si usas HTTPS
)

if __name__ == "__main__":
    app.run(debug=True)