"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, FavoritePlanet, FavoriteCharacter
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()

    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())

    return jsonify({"planets": planets_serialized}), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = db.session.get(Planet, planet_id)

    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404

    return jsonify({"planet": planet.serialize()}), 200


@app.route('/planet', methods=['POST'])
def create_planet():
    data = request.get_json()

    if "name" not in data:
        return jsonify({"msg": "Name is required"}), 400

    planet = Planet(
        name=data["name"],
        population=data.get("population"),
        climate=data.get("climate"),
        diameter=data.get("diameter")
    )

    db.session.add(planet)
    db.session.commit()

    return jsonify({
        "msg": "Planet created",
        "planet": planet.serialize()
    }), 201


@app.route('/planet/<int:planet_id>', methods=['PATCH'])
def update_planet(planet_id):
    planet = db.session.get(Planet, planet_id)

    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404

    data = request.get_json()

    if "name" in data:
        planet.name = data["name"]
    if "population" in data:
        planet.population = data["population"]
    if "climate" in data:
        planet.climate = data["climate"]
    if "diameter" in data:
        planet.diameter = data["diameter"]

    db.session.commit()

    return jsonify({
        "msg": "Planet updated",
        "planet": planet.serialize()
    }), 200


@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = db.session.get(Planet, planet_id)

    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"msg": "Planet deleted"}), 200


@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()

    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())

    return jsonify({"characters": characters_serialized}), 200


@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):
    character = db.session.get(Character, character_id)

    if character is None:
        return jsonify({"msg": "Character not found"}), 404

    return jsonify({"character": character.serialize()}), 200


@app.route('/character', methods=['POST'])
def create_character():
    data = request.get_json()

    if "name" not in data:
        return jsonify({"msg": "Name is required"}), 400

    if "sex" not in data:
        return jsonify({"msg": "Sex is required"}), 400

    character = Character(
        name=data["name"],
        age=data.get("age"),
        height=data.get("height"),
        weight=data.get("weight"),
        sex=data["sex"]
    )

    db.session.add(character)
    db.session.commit()

    return jsonify({
        "msg": "Character created",
        "character": character.serialize()
    }), 201


@app.route('/character/<int:character_id>', methods=['PATCH'])
def update_character(character_id):
    character = db.session.get(Character, character_id)

    if character is None:
        return jsonify({"msg": "Character not found"}), 404

    data = request.get_json()

    if "name" in data:
        character.name = data["name"]
    if "age" in data:
        character.age = data["age"]
    if "height" in data:
        character.height = data["height"]
    if "weight" in data:
        character.weight = data["weight"]
    if "sex" in data:
        character.sex = data["sex"]

    db.session.commit()

    return jsonify({
        "msg": "Character updated",
        "character": character.serialize()
    }), 200


@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = db.session.get(Character, character_id)

    if character is None:
        return jsonify({"msg": "Character not found"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({"msg": "Character deleted"}), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    if "email" not in data:
        return jsonify({"msg": "Email is required"}), 400

    if "password" not in data:
        return jsonify({"msg": "Password is required"}), 400

    if "name" not in data:
        return jsonify({"msg": "Name is required"}), 400

    user = User(
        email=data["email"],
        password=data["password"],
        name=data["name"],
        is_active=data.get("is_active", True)
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg": "User created",
        "user": user.serialize()
    }), 201


@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({"user": user.serialize()}), 200


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())

    return jsonify({"users": users_serialized}), 200


@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    favorite_planets = []
    for favorite in user.favorite_planets:
        favorite_planets.append(favorite.planet.serialize())

    favorite_characters = []
    for favorite in user.favorite_characters:
        favorite_characters.append(favorite.character.serialize())

    return jsonify({
        "user_id": user.id,
        "favorite_planets": favorite_planets,
        "favorite_characters": favorite_characters
    }), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):
    data = request.get_json()

    if "user_id" not in data:
        return jsonify({"msg": "User id is required"}), 400

    user = db.session.get(User, data["user_id"])
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404

    existing_favorite = FavoritePlanet.query.filter_by(
        user_id=user.id,
        planet_id=planet.id
    ).first()

    if existing_favorite:
        return jsonify({"msg": "Planet already in favorites"}), 400

    favorite = FavoritePlanet(
        user_id=user.id,
        planet_id=planet.id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites"}), 201


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def create_favorite_character(character_id):
    data = request.get_json()

    if "user_id" not in data:
        return jsonify({"msg": "User id is required"}), 400

    user = db.session.get(User, data["user_id"])
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    character = db.session.get(Character, character_id)
    if character is None:
        return jsonify({"msg": "Character not found"}), 404

    existing_favorite = FavoriteCharacter.query.filter_by(
        user_id=user.id,
        character_id=character.id
    ).first()

    if existing_favorite:
        return jsonify({"msg": "Character already in favorites"}), 400

    favorite = FavoriteCharacter(
        user_id=user.id,
        character_id=character.id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Character added to favorites"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    data = request.get_json()

    if "user_id" not in data:
        return jsonify({"msg": "User id is required"}), 400

    favorite = FavoritePlanet.query.filter_by(
        user_id=data["user_id"],
        planet_id=planet_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planet removed from favorites"}), 200


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    data = request.get_json()

    if "user_id" not in data:
        return jsonify({"msg": "User id is required"}), 400

    favorite = FavoriteCharacter.query.filter_by(
        user_id=data["user_id"],
        character_id=character_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "Favorite character not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Character removed from favorites"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
