from dataclasses import dataclass

@dataclass
class UniqueSearchHistorySchema:
    num_days: int
    country: str
    specific_places: str

    def to_dict(self):
        return {
            'num_days': self.num_days,
            'country': self.country,
            'specific_places': self.specific_places
        }

    def validate_data(data):
        if len(data.num_days) < 1:
            return False
        return True

@dataclass
class ItenerarySchema:
    unique_search_history_id: int
    day: str
    city: str
    travel_method: str
    travel_time: str
    morning_activity: str
    afternoon_activity: str
    evening_activity: str

    def to_dict(self):
        return {
            'unique_search_history_id': self.unique_search_history_id,
            'day': self.day,
            'city': self.city,
            'travel_method': self.travel_method,
            'travel_time': self.travel_time,
            'morning_activity': self.morning_activity,
            'afternoon_activity': self.afternoon_activity,
            'evening_activity': self.evening_activity
        }

    def validate_data(data):
        return True
