from marshmallow import ValidationError
from api import app, db
from flask import request, abort, jsonify
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError
from . import check_author_data
from api.schemas.author import author_schema, authors_schema


@app.post("/authors")
def create_author():
    try:
        # author_data = author_schema.loads(request.data)
        # author = AuthorModel(**author_data)

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
    authors_db = db.session.scalars(db.select(AuthorModel)).all()
    # authors = [author.to_dict() for author in authors_db]
    # return jsonify(authors), 200
    return jsonify(authors_schema.dump(authors_db)), 200


@app.get("/authors/<int:author_id>")
def get_author_by_id(author_id: int):
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    # return jsonify(author.to_dict()), 200
    return jsonify(author_schema.dump(author)), 200


@app.put("/authors/<int:author_id>")
def edit_author(author_id):
    data = request.json

    result = check_author_data(data)
    if not result[0]:
        abort(400, result[1].get("error"))

    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    try:
        for key, value in data.items():
            setattr(author, key, value)

        db.session.commit()
        return jsonify(author.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.delete("/authors/<int:author_id>")
def delete_author(author_id):
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
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    if request.method == "GET":
        quotes = [quote.to_dict() for quote in author.quotes]
        return jsonify({"author": author.name} | {"quotes": quotes}), 200

    elif request.method == "POST":
        data = request.json
        new_quote = QuoteModel(author, **data)
        db.session.add(new_quote)
        db.session.commit()
        return jsonify(new_quote.to_dict() | { "author_id" : author.id}), 201
    else:
        abort(405)