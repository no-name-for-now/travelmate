from datetime import date
from typing import List

from django.db import models
from pydantic import BaseModel


"""
General
"""


class AbstractBaseModel(models.Model):
    """Base model that gives children created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


"""
Models - used to store data in the database.
"""


class UniqueSearchHistoryORM(AbstractBaseModel):
    """Unique Search History model."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "specific_places", "num_days"],
                name="constraint__unique_search_history",
            )
        ]
        db_table = "unique_search_history"

    country = models.CharField(max_length=50)
    specific_places = models.CharField(max_length=100)
    num_days = models.IntegerField()

    @classmethod
    def from_api(cls, model: "UniqueSearchHistoryContract"):
        """
        Return a UniqueSearchHistory instance from an APIUniqueSearchHistory instance.
        """
        return cls(
            country=model.country,
            specific_places=model.specific_places,
            num_days=model.num_days,
        )

    def update_from_api(self, api_model: "UniqueSearchHistoryContract"):
        """
        Update the UniqueSearchHistory Django model from an APIUniqueSearchHistory instance.
        """
        self.country = api_model.country
        self.specific_places = api_model.specific_places
        self.num_days = api_model.num_days


class ItineraryORM(AbstractBaseModel):
    """Itinerary model."""

    class Meta:
        db_table = "itineraries"

    unique_search_history_id = models.ForeignKey(
        UniqueSearchHistoryORM, on_delete=models.CASCADE
    )
    day = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    travel_method = models.CharField(max_length=50)
    travel_time = models.CharField(max_length=50)
    morning_activity = models.CharField(max_length=150)
    afternoon_activity = models.CharField(max_length=150)
    evening_activity = models.CharField(max_length=150)

    @classmethod
    def from_api(
        cls, unique_search_history: "UniqueSearchHistoryORM", model: "ItineraryContract"
    ):
        """
        Return an Itinerary instance from an APIItinerary instance.
        """
        return cls(
            unique_search_history_id=unique_search_history.id,
            day=model.day,
            city=model.city,
            travel_method=model.travel_method,
            travel_time=model.travel_time,
            morning_activity=model.morning_activity,
            afternoon_activity=model.afternoon_activity,
            evening_activity=model.evening_activity,
        )

    def update_from_api(self, api_model: "ItineraryContract"):
        """
        Update the Itinerary Django model from an APIItinerary instance.
        """
        self.day = api_model.day
        self.city = api_model.city
        self.travel_method = api_model.travel_method
        self.travel_time = api_model.travel_time
        self.morning_activity = api_model.morning_activity
        self.afternoon_activity = api_model.afternoon_activity
        self.evening_activity = api_model.evening_activity


class WorldCitiesORM(AbstractBaseModel):
    """World Cities model."""

    class Meta:
        db_table = "world_cities"

    city = models.CharField(max_length=50)
    city_ascii = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    lat = models.FloatField()
    lng = models.FloatField()
    population = models.IntegerField()

    @classmethod
    def from_api(cls, model: "WorldCitiesContract"):
        """
        Return a WorldCities instance from an APIWorldCities instance.
        """
        return cls(
            city=model.city,
            city_ascii=model.city_ascii,
            country=model.country,
            iso2=model.iso2,
            iso3=model.iso3,
            lat=model.lat,
            lng=model.lng,
            population=model.population,
        )

    def update_from_api(self, api_model: "WorldCitiesContract"):
        """
        Update the WorldCities Django model from an APIWorldCities instance.
        """
        self.city = api_model.city
        self.city_ascii = api_model.city_ascii
        self.country = api_model.country
        self.iso2 = api_model.iso2
        self.iso3 = api_model.iso3
        self.lat = api_model.lat
        self.lng = api_model.lng
        self.population = api_model.population


class CityDescriptorsORM(AbstractBaseModel):
    """City Descriptors model."""

    class Meta:
        db_table = "city_descriptor"

    city_id = models.ForeignKey(WorldCitiesORM, on_delete=models.CASCADE)
    city_description = models.CharField(max_length=2000)

    @classmethod
    def from_api(cls, model: "CityDescriptorsContract"):
        """
        Return a CityDescriptors instance from an APICityDescriptors instance.
        """
        return cls(
            city_id=model.city_id,
            city_description=model.city_description,
        )

    def update_from_api(self, api_model: "CityDescriptorsContract"):
        """
        Update the CityDescriptors Django model from an APICityDescriptors instance.
        """
        self.city_id = api_model.city_id
        self.city_description = api_model.city_description


class SearchHistoryORM(AbstractBaseModel):
    """Search History model."""

    class Meta:
        db_table = "search_history"

    unique_search_history_id = models.ForeignKey(
        UniqueSearchHistoryORM, on_delete=models.CASCADE
    )

    @classmethod
    def from_api(cls, unique_search_history: "UniqueSearchHistoryORM"):
        """
        Return a SearchHistory instance from an APIUniqueSearchHistory instance.
        """
        return cls(
            unique_search_history_id=unique_search_history.id,
        )

    def update_from_api(self, api_model: "UniqueSearchHistoryORM"):
        """
        Update the SearchHistory Django model from an APIUniqueSearchHistory instance.
        """
        self.unique_search_history_id = api_model.id


class UserSavedItineraryORM(AbstractBaseModel):
    """User Saved Itinerary model."""

    class Meta:
        db_table = "user_saved_itinerary"

    user_id = models.IntegerField()
    ush_id = models.ForeignKey(UniqueSearchHistoryORM, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

    @classmethod
    def from_api(
        cls,
        unique_search_history: UniqueSearchHistoryORM,
        model: "UserSavedItineraryContract",
    ):
        """
        Return a UserSavedItinerary instance from an APIUserSavedItinerary instance.
        """
        return cls(
            user_id=model.user_id,
            ush_id=unique_search_history,
            from_date=model.from_date,
            to_date=model.to_date,
        )

    def update_from_api(self, api_model: "UserSavedItineraryContract"):
        """
        Update the UserSavedItinerary Django model from an APIUserSavedItinerary instance.
        """
        self.user_id = api_model.user_id
        self.ush_id = api_model.ush_id
        self.from_date = api_model.from_date
        self.to_date = api_model.to_date


"""
Types - used to return data from the API.
(a.k.a. contracts)
"""


# Itinerary contracts
class ItineraryContract(BaseModel):
    """Itinerary contract."""

    day: str
    city: str
    travel_method: str
    travel_time: str
    morning_activity: str
    afternoon_activity: str
    evening_activity: str

    @classmethod
    def from_model(cls, instance: ItineraryORM):
        """
        Convert a Django Itinerary model instance to an APIItinerary instance.
        """
        return cls(
            id=instance.id,
            day=instance.day,
            city=instance.city,
            travel_method=instance.travel_method,
            travel_time=instance.travel_time,
            morning_activity=instance.morning_activity,
            afternoon_activity=instance.afternoon_activity,
            evening_activity=instance.evening_activity,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "day": self.day,
            "city": self.city,
            "travel_method": self.travel_method,
            "travel_time": self.travel_time,
            "morning_activity": self.morning_activity,
            "afternoon_activity": self.afternoon_activity,
            "evening_activity": self.evening_activity,
        }


class APIItinerary(ItineraryContract):
    id: int


# UniqueSearchHistory contracts
class UniqueSearchHistoryContract(BaseModel):
    """Unique Search History contract."""

    country: str
    specific_places: str
    num_days: int

    @classmethod
    def from_model(cls, instance: UniqueSearchHistoryORM):
        """
        Convert a Django UniqueSearchHistory model instance to an APIUniqueSearchHistory instance.
        """
        return cls(
            id=instance.id,
            country=instance.country,
            specific_places=instance.specific_places,
            num_days=instance.num_days,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "country": self.country,
            "specific_places": self.specific_places,
            "num_days": self.num_days,
        }


class APIUniqueSearchHistory(UniqueSearchHistoryContract):
    id: int


# WorldCities contracts
class WorldCitiesContract(BaseModel):
    """World Cities contract."""

    city: str
    city_ascii: str
    country: str
    iso2: str
    iso3: str
    lat: float
    lng: float
    population: int

    @classmethod
    def from_model(cls, instance: WorldCitiesORM):
        """
        Convert a Django WorldCities model instance to an APIWorldCities instance.
        """
        return cls(
            id=instance.id,
            city=instance.city,
            city_ascii=instance.city_ascii,
            country=instance.country,
            iso2=instance.iso2,
            iso3=instance.iso3,
            lat=instance.lat,
            lng=instance.lng,
            population=instance.population,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "city_ascii": self.city_ascii,
            "country": self.country,
            "iso2": self.iso2,
            "iso3": self.iso3,
            "lat": self.lat,
            "lng": self.lng,
            "population": self.population,
        }


class APIWorldCities(WorldCitiesContract):
    id: int


# CityDescriptors contracts
class CityDescriptorsContract(BaseModel):
    """City Descriptors contract."""

    city_id: int
    city_description: str

    @classmethod
    def from_model(cls, instance: CityDescriptorsORM):
        """
        Convert a Django CityDescriptors model instance to an APICityDescriptors instance.
        """
        return cls(
            id=instance.id,
            city_id=instance.city_id,
            city_description=instance.city_description,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "city_description": self.city_description,
        }


class APICityDescriptors(CityDescriptorsContract):
    id: int


# SearchHistory contracts
class SearchHistoryContract(BaseModel):
    """Search History contract."""

    unique_search_history_id: int

    @classmethod
    def from_model(cls, instance: SearchHistoryORM):
        """
        Convert a Django SearchHistory model instance to an APISearchHistory instance.
        """
        return cls(
            id=instance.id,
            unique_search_history_id=instance.unique_search_history_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "unique_search_history_id": self.unique_search_history_id,
        }


class APISearchHistory(SearchHistoryContract):
    id: int


# UserSavedItinerary contracts
class UserSavedItineraryContract(BaseModel):
    """User Saved Itinerary contract."""

    user_id: str
    ush_id: int
    from_date: date
    to_date: date

    @classmethod
    def from_model(cls, instance: UserSavedItineraryORM):
        """
        Convert a Django UserSavedItinerary model instance to an APIUserSavedItinerary instance.
        """
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            ush_id=instance.ush_id,
            from_date=instance.from_date,
            to_date=instance.to_date,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ush_id": self.ush_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
        }


class APIUserSavedItinerary(UserSavedItineraryContract):
    id: int


class UserSearchContract(BaseModel):
    """User Search contract."""

    user_id: str
    ush_id: int
    from_date: date
    to_date: date
    country: str
    specific_places: str
    num_days: int

    @classmethod
    def from_model(
        cls,
        instance: UserSavedItineraryORM,
        unique_search_history: UniqueSearchHistoryORM,
    ):
        """
        Convert a Django UserSavedItinerary model instance to an APIUserSavedItinerary instance.
        """
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            ush_id=instance.ush_id,
            from_date=instance.from_date,
            to_date=instance.to_date,
            country=unique_search_history.country,
            specific_places=unique_search_history.specific_places,
            num_days=unique_search_history.num_days,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ush_id": self.ush_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "country": self.country,
            "specific_places": self.specific_places,
            "num_days": self.num_days,
        }


class APIUserSearch(UserSearchContract):
    id: int


"""
Listed responses - used to return lists of data from the API.
"""


# APIItineraryList contracts
class APIItineraryList(BaseModel):
    """API Itinerary List contract."""

    items: List[APIItinerary]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django Itinerary queryset to APIItinerary instances.
        """
        return cls(items=[APIItinerary.from_model(i) for i in qs])


# APIUniqueSearchHistoryList contracts
class APIUniqueSearchHistoryList(BaseModel):
    """API Unique Search History List contract."""

    items: List[APIUniqueSearchHistory]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django UniqueSearchHistory queryset to APIUniqueSearchHistory instances.
        """
        return cls(items=[APIUniqueSearchHistory.from_model(i) for i in qs])


# APIWorldCitiesList contracts
class APIWorldCitiesList(BaseModel):
    """API World Cities List contract."""

    items: List[APIWorldCities]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django WorldCities queryset to APIWorldCities instances.
        """
        return cls(items=[APIWorldCities.from_model(i) for i in qs])


# APICityDescriptorsList contracts
class APICityDescriptorsList(BaseModel):
    """API City Descriptors List contract."""

    items: List[APICityDescriptors]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django CityDescriptors queryset to APICityDescriptors instances.
        """
        return cls(items=[APICityDescriptors.from_model(i) for i in qs])


# APISearchHistoryList contracts
class APISearchHistoryList(BaseModel):
    """API Search History List contract."""

    items: List[APISearchHistory]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django SearchHistory queryset to APISearchHistory instances.
        """
        return cls(items=[APISearchHistory.from_model(i) for i in qs])


# APIUserSavedItineraryList contracts
class APIUserSavedItineraryList(BaseModel):
    """API User Saved Itinerary List contract."""

    items: List[APIUserSavedItinerary]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django UserSavedItinerary queryset to APIUserSavedItinerary instances.
        """
        return cls(items=[APIUserSavedItinerary.from_model(i) for i in qs])


# APIUserSearchList contracts
class APIUserSearchList(BaseModel):
    """API User Search List contract."""

    items: List[APIUserSearch]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django UserSearch queryset to APIUserSearch instances.
        """
        return cls(items=[APIUserSearch.from_model(i) for i in qs])
