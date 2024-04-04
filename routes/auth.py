from flask import Blueprint, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from database import db, db_create, db_delete
from models.user import User
import bcrypt


auth_bp = Blueprint('auth', __name__)


def hash_password(password):
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hashed_password.decode()


def check_password(password, user_password):
    return bcrypt.checkpw(str.encode(password), str.encode(user_password))


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    if username and password and name:
        user_exists = User.query.filter_by(username=username).first()
        if not user_exists:
            user = User(username=username,
                        password=hash_password(password),
                        name=name,
                        role='user')
            db_create(user)
            return jsonify({"message": "Usuário registrado com sucesso!"}), 201
        return jsonify({"message": "Nome de usuário não está disponível."}), 401
    return jsonify({"message": "Dados incompletos ou inválidos."}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and check_password(password, user.password):
            login_user(user)
            return jsonify({"message": f"Seja bem vindo, {user.name}!"})
    return jsonify({"message": "Usuário ou senha incorretos."}), 400


@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso. Até mais!"})


@auth_bp.route('/user/<uuid:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.json
    user = User.query.get_or_404(user_id)
    if user_id != current_user.id and current_user.role == 'user':
        return jsonify({"message": "Operação não permitida."}), 403
    if data.get('password'):
        user.password = hash_password(data.get('password'))
        db.session.commit()
        return jsonify({"message": "Senha alterada com sucesso!"})


@auth_bp.route('/user', methods=['GET'])
@login_required
def get_user():
    user = User.query.get_or_404(current_user.id)
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        }


@auth_bp.route('/user/<uuid:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role != 'admin' or user_id == current_user.id:
        return jsonify({"message": "Operação não permitida."}), 403
    db_delete(user)
    return jsonify({"message": "Usuário deletado com sucesso!"}), 204
