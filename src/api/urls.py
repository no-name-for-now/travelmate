from api import views
from api.models import APIUserSavedItinerary
from api.models import APIUserSearch
from fastapi import APIRouter


router = APIRouter()

# db_health GET

# get_user_search GET
# curl -X POST http://127.0.0.1:5000/get_user_search \
#      -H "Content-Type: application/json" \
#      -d '{
#            "user_id": "1"
#          }'
router.get(
    "/get_user_search",
    summary="Get a user's itinerary search history.",
    tags=["search"],
    response_model=APIUserSearch,
    name="search-get",
)(views.search_get)

# router.get(
#     "/get_user_search/",
#     summary="Get a user's search history.",
#     tags=["search"],

# )

# store_user_search POST
# curl -X POST http://127.0.0.1:5000/store_user_search \
#      -H "Content-Type: application/json" \
#      -d '{
#            "user_id": "1",
#            "ush_id": "1",
#            "from_date":"2023-11-02",
#            "to_date":"2023-11-05"
#          }'
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

# remote GET
