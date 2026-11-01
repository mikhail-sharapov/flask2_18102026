from sqlalchemy.exc import IntegrityError
from flask import abort, jsonify, request, Response, make_response
from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.models.role import RoleModel
from api.schemas.user import user_schema, users_schema


@app.get("/users/<int:user_id>")
def get_user_by_id(user_id: int):
    """
    Get User by id
    ---
    tags:
        - Users
    parameters:
         - in: path
           name: user_id
           type: integer
           required: true
           default: 1

    responses:
        200:
            description: A single user item
            schema:
                id: User
                properties:
                    id:
                        type: integer
                    username:
                        type: string
                    is_staff:
                        type: boolean
    """
    user = db.get_or_404(UserModel, ident=user_id, description=f"User with id={user_id} not found")
    response = make_response(user_schema.dump(user))
    response.status_code = 200
    response.headers["Custom-Header"] = "Gettin user by id"
    return response
    # return jsonify(user_schema.dump(user)), 200


@app.get("/users")
def get_users():
    """
    Get all Users
    ---
    tags:
        - Users
    """
    users = db.session.scalars(db.select(UserModel)).all()
    return jsonify(users_schema.dump(users)), 200


@app.post("/users")
def create_user():
    """Create user"""
    try:
        user = user_schema.loads(request.data)
    except ValidationError as e:
        abort(400, f"Validation error: {str(e)}")

    user.save()
    return jsonify(user_schema.dump(user)), 201


@app.post("/users/<int:user_id>/roles/<int:role_id>")
def add_role_to_user(user_id, role_id):
    """Add role to user"""
    user = db.get_or_404(UserModel, user_id, description=f"User with id={user_id} not found")
    role = db.get_or_404(RoleModel, role_id, description=f"Role with id={role_id} not found")
    try:
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
    except IntegrityError as ie:
        return jsonify(error=str(ie))
    return jsonify(result=f"Role '{role.name}' added to user '{user.username}'"), 201

