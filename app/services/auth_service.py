from app.models.user_model import get_user_by_username

def login_user(username, password):
    user = get_user_by_username(username)
    if user and user['password'] == password:
        return user
    return None
