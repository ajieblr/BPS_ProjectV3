from app import db
from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

class Testing(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    periode = db.Column(db.String(250), nullable=False)
    judul = db.Column(db.String(250),nullable=False)
    category = db.Column(db.String(100), nullable=True)
    sentimen = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<testing {}>'.format(self.id)