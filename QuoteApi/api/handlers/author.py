from marshmallow import EXCLUDE, ValidationError
from api import app, db, token_auth, multi_auth
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, authors_schema, edit_author_schema, AuthorSchema


@app.post("/authors")
# @multi_auth.login_required(role="admin")
@app.input(AuthorSchema, arg_name="author")
@app.output(AuthorSchema, status_code=201)
@app.doc(summary="Create new author", description="Create new authors", tags=["authors"])
def create_author(author):
    """Create new author"""
    # try:
    #     # при установке параметра load_instance=True сразу получаем экземпляр класса-модели
    #     author = author_schema.loads(request.data)
    #     db.session.add(author)
    #     db.session.commit()
    # except ValidationError as ve:
    #     abort(400, f"Validation error: {str(ve)}")
    # except Exception as e:
    #     abort(503, f"Database error: {str(e)}")
    # return jsonify(author_schema.dump(author)), 201
    try:
        db.session.add(author)
        db.session.commit()
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return author


@app.get("/authors")
@app.output(AuthorSchema(many=True), status_code=200)
@app.doc(summary="Get all authors", description="Get all authors", tags=["authors"])
def get_authors():
    """Get all authors"""
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    # return jsonify(authors_schema.dump(authors_db)), 200
    return authors_db


@app.get("/authors/<int:author_id>")
@app.output(AuthorSchema, status_code=200)
@app.doc(summary="Get author by id", description="Get author by id", tags=["authors"])
def get_author_by_id(author_id: int):
    """Get author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    # return jsonify(author_schema.dump(author)), 200
    return author


@app.put("/authors/<int:author_id>")
# @multi_auth.login_required
@app.input(AuthorSchema(load_instance=False), arg_name="author_data")
@app.output(AuthorSchema, status_code=201)
@app.doc(summary="Edit author", description="Edit authors", tags=["authors"])
def edit_author(author_id, author_data):
    """Edit author by id"""
    # try:
    #     new_data = edit_author_schema.load(request.json, unknown=EXCLUDE)
    # except ValidationError as ve:
    #     return abort(400, f"Validation error: {str(ve)}")
    
    # if not new_data:
    #     return abort(400, "No valid data to update")

    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    try:
        for key, value in author_data.items():
            setattr(author, key, value)

        db.session.commit()
        return author
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.delete("/authors/<int:author_id>")
# @multi_auth.login_required
@app.output(AuthorSchema, status_code=204)
@app.doc(summary="Delete author", description="Delete authors", tags=["authors"])
def delete_author(author_id):
    """Delete author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return jsonify({"message": f"Author with id {author_id} has deleted."})
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")

