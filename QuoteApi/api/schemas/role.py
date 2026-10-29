from api import ma
from api.models.role import RoleModel


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel

    id = ma.auto_field()
    name = ma.auto_field()