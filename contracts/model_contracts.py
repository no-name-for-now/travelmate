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