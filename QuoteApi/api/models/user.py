from flask import abort
from passlib.apps import custom_app_context as pwd_context
import sqlalchemy.orm as so
from api import db
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from itsdangerous import URLSafeSerializer, BadSignature
from config import Config


class UserModel(db.Model):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128))

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, f"Database integrity error: {str(e.orig)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(503, f"Database error: {str(e)}")

    def delete(self):
        try:
            db.session.delete()
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(503, f"Database error: {str(e)}")

    def generate_auth_token(self):
        s = URLSafeSerializer(Config.SECRET_KEY)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = URLSafeSerializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except BadSignature:
            return None  # invalid token
        user = db.one_or_404(UserModel, data['id'])
        return user