from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flasgger import Swagger

# Eklentileri burada tanımlıyoruz
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
swagger = Swagger()