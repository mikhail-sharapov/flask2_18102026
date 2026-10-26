from api import app
from api. models.user import UserModel


app.get("/users/<int:user_id>")
def get_user_by_id(user_id: int):
    """Get user by id"""
    pass


app.get("/users")
def get_users():
    """Get all users"""
    pass


app.post("/users")
def create_user():
    """Create user"""
    pass