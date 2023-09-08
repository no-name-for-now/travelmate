from database import db 
from sqlalchemy import PrimaryKeyConstraint

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_days = db.Column(db.Integer)
    country = db.Column(db.String(50), nullable=False)
    specific_places = db.Column(db.String(100), nullable=False)
    day = db.Column(db.String(50))
    travel_method = db.Column(db.String(50))
    travel_time = db.Column(db.String(50))
    morning_activity = db.Column(db.String(100))
    afternoon_activity = db.Column(db.String(100))
    evening_activity = db.Column(db.String(100))

    __table_args__ = (
        PrimaryKeyConstraint('country', 'specific_places', 'num_days'),
    )
