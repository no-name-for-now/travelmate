from database import db 
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime

class Itenerary(db.Model):
    __tablename__ = 'iteneraries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_search_history_id = db.Column(db.Integer, db.ForeignKey('unique_search_history.id', ondelete='CASCADE'), nullable=False)
    day = db.Column(db.String(50))
    city = db.Column(db.String(50))
    travel_method = db.Column(db.String(50))
    travel_time = db.Column(db.String(50))
    morning_activity = db.Column(db.String(150))
    afternoon_activity = db.Column(db.String(150))
    evening_activity = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



class UniqueSearchHistory(db.Model):
    __tablename__ = 'unique_search_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_days = db.Column(db.Integer)
    country = db.Column(db.String(50), nullable=False)
    specific_places = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('country', 'specific_places', 'num_days'),
    )

class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_search_history_id = db.Column(db.Integer, db.ForeignKey('unique_search_history.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
