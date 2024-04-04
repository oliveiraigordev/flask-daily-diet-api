from flask import Flask
from flask_login import LoginManager
from database import db
from models.diet import Diet
from models.user import User
from routes.auth import auth_bp
from routes.diet import diet_bp


app = Flask(__name__)
login_manager = LoginManager()

app.config.from_pyfile('settings.py')
app.register_blueprint(auth_bp)
app.register_blueprint(diet_bp)

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)
