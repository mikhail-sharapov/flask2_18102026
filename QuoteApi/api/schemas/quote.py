from marshmallow import EXCLUDE, ValidationError
from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema
from marshmallow.validate import Length



def rating_validate(value: int):
    """Функция-пример ручной валидации"""
    if value not in range(1, 6):
        raise ValidationError("Rating not in range 1-5")


class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        dump_only = ("id",)
        unknown = EXCLUDE

    id = ma.auto_field()
    text = ma.auto_field(required=True, validate=Length(min=3))
    author_id = ma.auto_field()
    author = ma.Nested(AuthorSchema(only=("name","surname")))
    rating = ma.auto_field(validate=rating_validate) #strict=True,


quote_schema = QuoteSchema(exclude=["author_id"])
quotes_schema = QuoteSchema(many=True, exclude=["author"])

edit_quote_without_rating_schema = QuoteSchema(exclude=["rating"], partial=True)

filter_quote_schema = QuoteSchema(partial=True, exclude=["author"])