def insert_data(model, db, dict):
    data = model(**dict)
    db.session.add(data)
    db.session.commit()
