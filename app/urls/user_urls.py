from app import app
from app.views.user_view import create_dummy_users


@app.route('/create_users', methods=['POST'])
def add_user():
    return create_dummy_users()
