def list_tables(db):
    # Get a list of all tables in the database
    inspector = db.inspect(db.engine)
    table_names = inspector.get_table_names()
    
    return table_names

def query_search_history(model, country, specific_places, num_days):
    # Use the SQLAlchemy filter method to specify your filter criteria
    data = model.query.filter(
        model.country == country,
        model.specific_places == specific_places,
        model.num_days == num_days
    ).all()
    
    # Process the filtered data (for example, print it)
    for item in data:
        return item.id
