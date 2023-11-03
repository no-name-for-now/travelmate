from api import views
from api.models.user_saved_itinerary import APIUserSavedItinerary
from api.models.user_search import APIUserSearchList
from fastapi import APIRouter


router = APIRouter()


router.get(
    "/get_user_search",
    summary="Get a user's itinerary search history.",
    tags=["search"],
    response_model=APIUserSearchList,
    name="search-get",
)(views.search_get)

router.post(
    "/store_user_search",
    summary="Store a user's search history.",
    tags=["search"],
    response_model=APIUserSavedItinerary,
    name="search-post",
)(views.search_post)

# get_city_description POST
# curl -X POST https://resolute-tracer-402011.ey.r.appspot.com/get_city_description \
#      -H "Content-Type: application/json" \
#      -d '{
#            "country": "Belgium",
#            "cities": "Brussels"
#          }'

# first_backend POST
# curl -X POST http://127.0.0.1:5000/first_backend \
#      -H "Content-Type: application/json" \
#      -d '{
#            "country": "Belgium",
#            "city": "Brussels",
#            "days": 3
#          }'

# top10 GET
