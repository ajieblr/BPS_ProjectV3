from app import db
from datetime import datetime

class Berita(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    periode = db.Column(db.String(250), nullable=False)
    label = db.Column(db.String(60), nullable=False)
    headline = db.Column(db.String(250),nullable=False)
    content = db.Column(db.String(10000),nullable=True)
    predik = db.Column(db.String(100), nullable=True)
    sentimen = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    link = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Berita {}>'.format(self.id)