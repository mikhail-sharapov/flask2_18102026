from flask import jsonify
from api import app, db, basic_auth
from api.models.user import UserModel
from api.schemas.token import TokenOut


@app.route('/auth/token')
@app.auth_required(basic_auth)
@app.output(TokenOut, status_code=200)
@app.doc(summary="Get token for auth", description="Get token for auth", tags=["token"], responses=[200, 401, 404])
def get_auth_token():
   """Get token for auth"""
   user = basic_auth.current_user
   user = db.one_or_404(db.select(UserModel).filter_by(username=user.username))
   token = user.generate_auth_token()
   return {"token": token}
