from flask.ext.login import LoginManager

from leiquery import app
from .database import session
from .models import  User

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_get"
login_manager.login_message_category = "danager"

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))