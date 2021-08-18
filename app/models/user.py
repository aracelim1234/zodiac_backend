from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birthday = db.Column(db.String)
    about_me = db.Column(db.String)
    username = db.Column(db.String, nullable=False, unique=True)
    # email = db.Column(db.String)
    password1 = db.Column(db.String, nullable=False)
    password2 = db.Column(db.String)

    def to_json_user(self):
        return {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "birthday": self.birthday,
            "about me": self.about_me,
            "username": self.username,
            # "email": self.email,
            "password": self.password1
        }


 
    