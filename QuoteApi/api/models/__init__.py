from api import db
import sqlalchemy as sa


users_roles = db.Table(
    "users_roles",
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id")),
    sa.UniqueConstraint('user_id', 'role_id', name='unique_user_role_relation')
    )