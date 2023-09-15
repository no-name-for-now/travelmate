def list_tables(db):
    # Get a list of all tables in the database
    inspector = db.inspect(db.engine)
    table_names = inspector.get_table_names()
    
    return table_names



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

