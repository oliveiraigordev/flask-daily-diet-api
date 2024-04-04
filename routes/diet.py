from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from database import db, db_create, db_delete
from models.diet import Diet


diet_bp = Blueprint('diet', __name__)


@diet_bp.route('/meal', methods=['POST'])
@login_required
def create_meal():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    datetime = data.get('datetime')
    is_diet = data.get('is_diet')

    if name and description and datetime and is_diet is not None:
        meal = Diet(
            username=current_user.id,
            name=name,
            description=description,
            datetime=datetime,
            is_diet=is_diet
            )
        db_create(meal)
        return jsonify({"message": "Refeição registrada com sucesso!"}), 201
    return jsonify({"message": "Dados incompletos ou inválidos"}), 401


@diet_bp.route('/meal', methods=['GET'])
@login_required
def get_meals():
    meals = Diet.query.filter_by(username=current_user.id)
    meals_list = []
    for meal in meals:
        meals_list.append({
                "id": meal.id,
                "name": meal.name,
                "description": meal.description,
                "datetime": meal.datetime,
                "is_diet": meal.is_diet
            })
    return jsonify({"meals": meals_list, "meals_number": len(meals_list)})


@diet_bp.route('/meal/<uuid:meal_id>', methods=['GET'])
@login_required
def get_meal(meal_id):
    meal = Diet.query.get_or_404(meal_id)
    if meal.username != current_user.id:
        return jsonify({"message": "Acesso negado à este registro."}), 401
    return {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "datetime": meal.datetime,
            "is_diet": meal.is_diet
        }


@diet_bp.route('/meal/<uuid:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Diet.query.get_or_404(meal_id)
    if meal.username != current_user.id:
        return jsonify({"message": "Acesso negado à este registro."}), 401
    db_delete(meal)
    return jsonify({"message": "Refeição excluída com sucesso!"}), 204


@diet_bp.route('/meal/<uuid:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    datetime = data.get('datetime')
    is_diet = data.get('is_diet')
    meal = Diet.query.get_or_404(meal_id)
    if meal.username != current_user.id:
        return jsonify({"message": "Acesso negado à este registro."}), 401
    if name:
        meal.name = name
    if description:
        meal.descripion = description
    if datetime:
        meal.datetime = datetime
    if is_diet is not None:
        meal.is_diet = is_diet
    db.session.commit()
    return jsonify({"message": "Refeição atualizada com sucesso!"})
