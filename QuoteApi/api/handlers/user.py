from sqlalchemy.exc import IntegrityError
from flask import abort, jsonify, request, Response, make_response
from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.models.role import RoleModel
from api.schemas.user import user_schema, users_schema, UserSchema
from flask_babel import _


@app.get("/users/<int:user_id>")
@app.output(UserSchema, status_code=200)
@app.doc(summary="Get user by id", description="Get user by id", tags=["users"], responses=[200])
def get_user_by_id(user_id: int):
    """Get iser by id"""
    user = db.get_or_404(UserModel, ident=user_id, description=_("User with id=%(user_id)s not found", user_id=user_id))
    return user


@app.get("/users")
@app.output(UserSchema(many=True), status_code=200)
@app.doc(summary="Get all users", description="Get all users", tags=["users"])
def get_users():
    """Get all users"""
    users = db.session.scalars(db.select(UserModel)).all()
    return users


@app.post("/users")
@app.input(UserSchema, arg_name="user", example={"username": "new_user", "password": "new_password"})
@app.output(UserSchema, status_code=201)
@app.doc(summary="Create new user", description=_("Create new user and save to db"), tags=["users"], responses=[400, 503])
def create_user(user):
    """Create user"""
    user.save()
    return user


@app.post("/users/<int:user_id>/roles/<int:role_id>")
@app.doc(summary="Add role to user", description="Add role to user", tags=["users"], responses=[201,404])
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

