from api import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from api.models import users_roles


class RoleModel(db.Model):
    __tablename__ = "roles"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32) ,index=True, unique=True)
    users: so.Mapped[list['UserModel']] = so.relationship(secondary=users_roles, back_populates='roles') # type: ignore

    def __init__(self, name):
        self.name = name
        


