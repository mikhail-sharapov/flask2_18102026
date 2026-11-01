from sqlalchemy.exc import IntegrityError
from flask import abort, jsonify, request, Response, make_response
from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.models.role import RoleModel
from api.schemas.user import user_schema, users_schema, UserSchema


@app.get("/users/<int:user_id>")
@app.output(UserSchema)
@app.doc(summary="Get user by id", description="Get user by id", tags=["users"])
def get_user_by_id(user_id: int):
    """Get iser by id"""
    user = db.get_or_404(UserModel, ident=user_id, description=f"User with id={user_id} not found")
    # response = make_response(user)
    # response.status_code = 200
    # response.headers["Custom-Header"] = "Gettin user by id"
    # return response
    return user, 200


@app.get("/users")
@app.output(UserSchema(many=True))
@app.doc(summary="Get all users", description="Get all users", tags=["users"])
def get_users():
    """Get all users"""
    users = db.session.scalars(db.select(UserModel)).all()
    return users, 200


@app.post("/users")
@app.input(UserSchema, arg_name="user", example={"username": "new_user", "password": "new_password"})
@app.output(UserSchema, status_code=201)
@app.doc(summary="Create new user", description="Create new user", tags=["users"], responses=[400, 503])
def create_user(user):
    """Create user"""
    # try:
    #     user = user_schema.loads(request.data)
    # except ValidationError as e:
    #     abort(400, f"Validation error: {str(e)}")
    user.save()
    # return jsonify(user_schema.dump(user)), 201
    return user


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

