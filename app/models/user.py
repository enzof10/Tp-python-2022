from datetime import datetime
from utils.db import db

# el orm coloca el nombre de la tabla con la clase
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    # created_at = db.Column(db.DateTime, nullable=False)
    # updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        # self.created_at = datetime.datetime.now()
        # self.updated_at = datetime.datetime.now()
