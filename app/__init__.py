from flask import Flask


from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager

app = Flask(__name__, template_folder='../templates', static_folder='../static')


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# jwt = JWTManager(app)


from app.model import berita, testing, user

from app import routes