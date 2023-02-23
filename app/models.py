from app import db

class TRY(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(500))
