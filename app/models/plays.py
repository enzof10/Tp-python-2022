from utils.db import db


class Play_number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    attemp = db.Column(db.Integer)
    is_winner = db.Column(db.Boolean)
    numbers = db.Column(db.String(100))
    date = db.Column(db.DateTime)

    def __init__(self, game_id, attemp, is_winner, numbers , date):
        self.game_id = game_id
        self.attemp = attemp
        self.is_winner = is_winner
        self.numbers = numbers
        self.date = date