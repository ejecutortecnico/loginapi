from flask import Flask
from flask_login import LoginManager
from models import User
from routes.login import auth_bp
from routes.usuarios import usuarios_bp

app = Flask(__name__)
app.secret_key = "clave_secreta"

login_manager = LoginManager(); 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(usuarios_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)