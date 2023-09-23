from sqlalchemy import func
from flask import jsonify
import json


def list_tables(db):
    # Get a list of all tables in the database
    inspector = db.inspect(db.engine)
    table_names = inspector.get_table_names()
    
    return table_names



def query_search_fe(model, **kwargs):
    query = model.query

    for column, value in kwargs.items():
        query = query.filter(getattr(model, column) == value)

    data = query.all()
    if len(data) == 1:
        for item in data:
            return item.id 
    else:
        print(data)
        for item in data:
            print(item)

        results = [item.to_dict() for item in data] if data else []
        json_string = json.dumps(results, indent=4) 
        print(json_string)
        return json_string

def query_search(model, **kwargs):
    query = model.query

    for column, value in kwargs.items():
        query = query.filter(getattr(model, column) == value)

    data = query.all()

    if len(data) == 1:
        for item in data:
            return item.id 
    else: 
        return data

def most_searched(db, SearchHistory, UniqueSearchHistory):
    # Create a subquery to count the rows for each unique_search_history_id
    subquery = (
        db.session.query(
            SearchHistory.unique_search_history_id,
            func.count(SearchHistory.id).label("row_count")
        )
        .group_by(SearchHistory.unique_search_history_id)
        .subquery()
    )
    
    # Query to retrieve the country, specific places, number of days, and row count
    result = (
        db.session.query(
            UniqueSearchHistory.country,
            UniqueSearchHistory.specific_places,
            UniqueSearchHistory.num_days,
            subquery.c.row_count
        )
        .join(subquery, UniqueSearchHistory.id == subquery.c.unique_search_history_id)
        .order_by(subquery.c.row_count.desc())
        .limit(10)  # Limit to the top 10 entries
        .all()
    )
    
    # Check if there is a result
    if result:
        return result
    else:
        print("No data found")
