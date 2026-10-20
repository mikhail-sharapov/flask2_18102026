from api import app, db
from flask import jsonify
from api.models.quote import QuoteModel


@app.get("/quotes")
def get_quotes():
    """ Функция возвращает все цитаты из БД. """
    quotes_db = db.session.scalars(db.select(QuoteModel)).all()
    # Формируем список словарей
    quotes = []
    for quote in quotes_db:
        quotes.append(quote.to_dict())
    return jsonify(quotes), 200