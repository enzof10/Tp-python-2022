from utils.db import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    points = db.Column(db.Integer)
    is_winner = db.Column(db.Boolean)
    attemps = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    duration = db.Column(db.Integer)

    def __init__(self, user_id, points, is_winner, start, end, duration, attemps):
        self.user_id = user_id
        self.points = points
        self.is_winner = is_winner
        self.start = start
        self.end = end
        self.duration = duration
        self.attemps = attemps
