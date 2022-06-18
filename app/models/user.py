from datetime import datetime
from utils.db import db

# un usuario tiene muchos juegos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.relationship('Game', backref='user', lazy='dynamic')
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

