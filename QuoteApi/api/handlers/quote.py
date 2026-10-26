from api import app, db, auth
from flask import jsonify, request, abort
from api.models.quote import QuoteModel
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.quote import quote_schema, quotes_schema, filter_quote_schema
from marshmallow import EXCLUDE, RAISE, ValidationError
from api.models.author import AuthorModel


@app.get("/quotes")
def get_quotes():
    """Get all quotes"""
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    return jsonify(quotes_schema.dump(quotes_db)), 200


@app.get("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id: int):
    """Get quote by id"""
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")
    return jsonify(quote_schema.dump(quote)), 200


@app.get("/quotes/count")
def get_quotes_count() -> int:
    """Get count of quotes"""
    count = db.session.scalar(func.count(QuoteModel.id))
    return jsonify(count=count), 200


@app.put("/quotes/<int:quote_id>")
def edit_quote(quote_id: int):
    """Edit quote by id"""
    try:
        new_data = quote_schema.load(request.json, unknown=EXCLUDE)
    except ValidationError as ve:
        return abort(400, f"Validation error: {str(ve)}")
    
    if not new_data:
        return abort(400, "No valid data to update")

    quote = db.get_or_404(QuoteModel, quote_id, description=f"Quote with id={quote_id} not found")

    try:
        for key, value in new_data.items():
            setattr(quote, key, value)

        db.session.commit()
        return jsonify(quote_schema.dump(quote)), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    """Delete quote by id """
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")
    db.session.delete(quote)
    try:
        db.session.commit()
        return jsonify({"message": f"Quote with id {quote_id} has deleted."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
    
    
@app.route("/quotes/filter", methods=['GET'])
def filter_quotes():
    """Get quotes by filters"""
    try:
        data = filter_quote_schema.load(request.args, unknown=RAISE)
        quotes = db.session.scalars(db.select(QuoteModel).filter_by(**data)).all()
    except ValidationError as ve:
        abort(400, f"Validation error: {str(ve)}")
    
    return jsonify(quotes_schema.dump(quotes)), 200


@app.route("/authors/<int:author_id>/quotes", methods=["GET", "POST"])
@auth.login_required
def author_quotes(author_id: int):
    """Get all quotes of author by id. Create new quote of author"""
    # print(f"user = {auth.current_user()}")

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