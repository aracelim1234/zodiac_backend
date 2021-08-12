from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birthday = db.Column(db.String)
    username = db.Column(db.String, nullable=False, unique=True)
    # email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

    def to_json_user(self):
        return {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "birthday": self.birthday,
            "username": self.username,
            # "email": self.email,
            "password": self.password
        }


 
    