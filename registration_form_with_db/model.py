from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # установка шифрованного пароля, используем функцию generate_password_hash из модуля werkzeug.security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # проверка пароля, используем функцию check_password_hash из модуля werkzeug.security
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)