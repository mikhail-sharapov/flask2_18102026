from flask import jsonify
from api import app, db, multi_auth
from api.models.user import UserModel


@app.route('/auth/token')
@multi_auth.login_required
def get_auth_token():
   user = multi_auth.current_user()
   user = db.one_or_404(db.select(UserModel).filter_by(username=user.username))
   token = user.generate_auth_token()
   return jsonify({'token': token}), 200