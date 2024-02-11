from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

login_manager = LoginManager()
db = SQLAlchemy()
load_dotenv()