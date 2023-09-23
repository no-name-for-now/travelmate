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

    def to_dict(self):
        return {
            'id': self.id,
            'unique_search_history_id': self.unique_search_history_id,
            'day': self.day,
            'city': self.city,
            'travel_method': self.travel_method,
            'travel_time': self.travel_time,
            'morning_activity': self.morning_activity,
            'afternoon_activity': self.afternoon_activity,
            'evening_activity': self.evening_activity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }



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

#source https://simplemaps.com/data/world-cities
class WorldCities(db.Model):
    __tablename__ = 'world_cities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(50))
    city_ascii = db.Column(db.String(50))
    country = db.Column(db.String(50))
    iso2 = db.Column(db.String(2))
    iso3 = db.Column(db.String(3))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    population = db.Column(db.Integer)

