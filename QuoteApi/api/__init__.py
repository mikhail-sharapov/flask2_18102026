from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.json.ensure_ascii = False
app.config.from_object("config.DevConfig")

db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)
ma = Marshmallow()
ma.init_app(app)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme="Bearer")
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
   from api.models.user import UserModel
   user = db.one_or_404(db.select(UserModel).filter_by(username=username))
   if not user or not user.verify_password(password):
       return False
   g.user = user
   return True


@token_auth.verify_token
def verify_token(token):
   from api.models.user import UserModel
   user = UserModel.verify_auth_token(token)
   print(f"{user=}")
   return user


# DONE. Обязательно добавить импорт для обработчиков
from api.handlers import author, quote, user, token
