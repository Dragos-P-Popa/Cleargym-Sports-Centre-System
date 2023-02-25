from app import db


class TRY(db.Model):
    # Worth noting, string input seems to be automatically converted to an int
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(500))
