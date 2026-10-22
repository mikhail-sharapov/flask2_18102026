from marshmallow import Schema, fields


class SAuthor(Schema):
    id = fields.Integer(strict=True)
    name = fields.String(required=True, error_messages={"required": "field 'name' is required"})
    surname = fields.String()
    email = fields.Email(required=True, error_messages={"required": "field 'email' is required"})