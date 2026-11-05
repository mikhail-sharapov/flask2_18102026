from api import app, db, token_auth
from flask import jsonify, request, abort
from api.models.quote import QuoteModel
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from api.schemas.quote import quote_schema, quotes_schema, filter_quote_schema, QuoteSchema
from marshmallow import EXCLUDE, RAISE, ValidationError
from api.models.author import AuthorModel
from apiflask.fields import String, Integer


@app.get("/quotes")
@app.output(QuoteSchema(many=True), status_code=200)
@app.doc(summary="Get all quotes", description="Get all quotes", tags=["quotes"], responses=[200])
def get_quotes():
    """Get all quotes"""
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    return quotes_db


@app.get("/quotes/<int:quote_id>")
@app.output(QuoteSchema, status_code=200)
@app.doc(summary="Get quote by id", description="Get quote by id", tags=["quotes"], responses=[200, 404])
def get_quote_by_id(quote_id: int):
    """Get quote by id"""
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")
    return quote


@app.get("/quotes/count")
@app.output(schema={"count": Integer()}, status_code=200)
@app.doc(summary="Get count of quotes", description="Get count of quotes", tags=["quotes"], responses=[200])
def get_quotes_count() -> int:
    """Get count of quotes"""
    count = db.session.scalar(func.count(QuoteModel.id))
    return {"count": count}


@app.put("/quotes/<int:quote_id>")
@app.auth_required(token_auth, ["admin", "user"])
@app.input(QuoteSchema(load_instance=False, partial=True), arg_name="quote_data")
@app.output(QuoteSchema, status_code=201)
@app.doc(summary="Edit quote by id", description="Edit quote by id", tags=["quotes"], responses=[201,404,503])
def edit_quote(quote_id: int, quote_data):
    """Edit quote by id"""
    quote = db.get_or_404(QuoteModel, quote_id, description=f"Quote with id={quote_id} not found")

    try:
        for key, value in quote_data.items():
            setattr(quote, key, value)

        db.session.commit()
        return quote
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")


@app.delete("/quotes/<int:quote_id>")
@app.auth_required(token_auth, ["admin", "user"])
@app.output(schema={"message": String()}, status_code=200)
@app.doc(summary="Delete quote by id", description="Delete quote by id", tags=["quotes"], responses=[200,404,503])
def delete_quote(quote_id):
    """Delete quote by id"""
    quote = db.get_or_404(entity=QuoteModel, ident=quote_id, description=f"Quote with id={quote_id} not found")
    db.session.delete(quote)
    try:
        db.session.commit()
        return {"message": f"Quote with id {quote_id} has deleted."}
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")
    
    
@app.get("/quotes/filter")
@app.input(QuoteSchema(exclude=["author"], partial=True), location="query", arg_name="filter_data")
@app.output(QuoteSchema(many=True), status_code=200)
@app.doc(summary="Get quotes by filters", description="Get quotes by filters", tags=["quotes"], responses=[200])
def filter_quotes(filter_data):
    """Get quotes by filters"""
    quotes = db.session.scalars(db.select(QuoteModel).filter_by(**filter_data)).all()
    return quotes


@app.get("/authors/<int:author_id>/quotes")
@app.output(QuoteSchema(many=True), status_code=200)
@app.doc(summary="Get all quotes of author by id", description="Get all quotes of author by id", tags=["quotes"], responses=[200])
def get_author_quotes(author_id: int):
    """Get all quotes of author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")
    return author.quotes


@app.post("/authors/<int:author_id>/quotes")
@app.auth_required(token_auth, ["admin", "user"])
@app.input(QuoteSchema(exclude=["author", "author_id"], partial=True, load_instance=False), arg_name="quote_data")
@app.output(QuoteSchema, status_code=201)
@app.doc(summary="Create new quote of author by id", description="Create new quote of author by id", tags=["quotes"],
         responses=[201,404,422,500,503])
def create_author_quote(author_id: int, quote_data):
    """Create new quote of author by id"""
    author = db.get_or_404(AuthorModel, author_id, description=f"Author with id={author_id} not found")

    try:
        new_quote = QuoteModel(author, **quote_data)
        db.session.add(new_quote)
        db.session.commit()
    except TypeError as te:
        abort(500, f"Validating error: {str(te)}")        
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(503, f"Database error: {str(e)}")

    return new_quote
