from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema


def rating_validate(value: int):
    """Функция-пример ручной валидации"""
    return value in range(1, 6)


class QuoteSchema(ma.SQLAlchemySchema):
   class Meta:
       model = QuoteModel

   id = ma.auto_field()
   text = ma.auto_field()
   author = ma.Nested(AuthorSchema(only=("name",)))
   rating = ma.Integer(strict=True, validate=rating_validate)


quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)