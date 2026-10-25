from marshmallow import EXCLUDE, ValidationError
from api import app, db
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.author import author_schema, authors_schema, edit_author_schema
from api.schemas.quote import quote_schema, quotes_schema


@app.post("/authors")
def create_author():
    """Create new author"""
    try:
        # при установке параметра load_instance=True сразу получаем экземпляр класса-модели
        author = author_schema.loads(request.data)
        db.session.add(author)
        db.session.commit()
    except ValidationError as ve:
        abort(400, f"Validation error: {str(ve)}")
    except Exception as e:
        abort(503, f"Database error: {str(e)}")
    return jsonify(author_schema.dump(author)), 201


@app.get("/authors")
def get_authors():
    """Get all authors"""
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    return jsonify(authors_schema.dump(authors_db)), 200


@app.get("/authors/<int:author_id>")
def get_author_by_id(author_id: int):
    """Get author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    return jsonify(author_schema.dump(author)), 200


@app.put("/authors/<int:author_id>")
def edit_author(author_id):
    """Edit author by id"""
    try:
        new_data = edit_author_schema.load(request.json, unknown=EXCLUDE)
    except ValidationError as ve:
        return abort(400, f"Validation error: {str(ve)}")
    
    if not new_data:
        return abort(400, "No valid data to update")

    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    try:
        for key, value in new_data.items():
            setattr(author, key, value)

        db.session.commit()
        return jsonify(author_schema.dump(author)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
    """Delete author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    db.session.delete(author)
    try:
        db.session.commit()
        return jsonify({"message": f"Author with id {author_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.route("/authors/<int:author_id>/quotes", methods=["GET", "POST"])
def author_quotes(author_id: int):
    """Get all quotes of author by id. Create new quote of author"""
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    if request.method == "GET":      
        return jsonify(quotes_schema.dump(author.quotes)), 200

    elif request.method == "POST":
        try:
            new_quote_data = quote_schema.loads(request.data)
            new_quote = QuoteModel(author, **new_quote_data)
            db.session.add(new_quote)
            db.session.commit()
        except ValidationError as ve:
            abort(400, f"Validating error: {ve.messages_dict}")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(503, f"Database error: {str(e)}")

        return jsonify(quote_schema.dump(new_quote)), 201
    else:
        abort(405)