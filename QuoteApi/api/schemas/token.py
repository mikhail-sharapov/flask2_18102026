from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length


class TokenOut(Schema):
    token = String(required=True, validate=Length(equal=115))