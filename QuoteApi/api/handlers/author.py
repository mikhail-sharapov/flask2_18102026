from marshmallow import EXCLUDE, ValidationError
from api import app, db, token_auth
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, authors_schema, edit_author_schema, AuthorSchema
from apiflask.fields import String
from flask_babel import _

@app.post("/authors")
@app.auth_required(token_auth, ["admin"])
@app.input(AuthorSchema, arg_name="author")
@app.output(AuthorSchema, status_code=201)
@app.doc(summary="Create new author", description="Create new authors", tags=["authors"], responses=[201,503])
def create_author(author):
    """Create new author"""
    try:
        db.session.add(author)
        db.session.commit()
    except Exception as e:
        abort(503, _("Database error: %(error)s", error=str(e)))
    return author


@app.get("/authors")
@app.output(AuthorSchema(many=True), status_code=200)
@app.doc(summary="Get all authors", description="Get all authors", tags=["authors"], responses=[200])
def get_authors():
    """Get all authors"""
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    return authors_db


@app.get("/authors/<int:author_id>")
@app.output(AuthorSchema, status_code=200)
@app.doc(summary="Get author by id", description="Get author by id", tags=["authors"], responses=[200])
def get_author_by_id(author_id: int):
    """Get author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=_("Author with id=%(author_id)s not found", author_id=author_id))
    return author


@app.put("/authors/<int:author_id>")
@app.auth_required(token_auth, ["admin"])
@app.input(AuthorSchema(load_instance=False, partial=True), arg_name="author_data")
@app.output(AuthorSchema, status_code=201)
@app.doc(summary="Edit author", description="Edit authors", tags=["authors"], responses=[201,404,503])
def edit_author(author_id, author_data):
    """Edit author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=_("Author with id=%(author_id)s not found", author_id=author_id))

    try:
        for key, value in author_data.items():
            setattr(author, key, value)

        db.session.commit()
        return author
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, _("Database error: %(error)s", error=str(e)))


@app.delete("/authors/<int:author_id>")
@app.auth_required(token_auth, ["admin"])
@app.output(schema={"message": String()}, status_code=200)
@app.doc(summary="Delete author", description="Delete authors", tags=["authors"], responses=[200,503])
def delete_author(author_id):
    """Delete author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=_("Author with id=%(author_id)s not found", author_id=author_id))
    db.session.delete(author)
    try:
        db.session.commit()
        return {"message": _("Author with id %(author_id)s has deleted.", author_id=author_id)}
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, _("Database error: %(error)s", error=str(e)))

