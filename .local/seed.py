import json
import os

import psycopg2


# Replace these variables with your actual values
db_config = {
    "dbname": "api",
    "user": "api",
    "password": "api",
    "host": "localhost",
    "port": "5432",
}

json_file_path = os.path.relpath("data/")
table_names = [
    "city_climate",
    "city_descriptor",
    "itineraries",
    "search_history",
    "unique_search_history",
    "user_saved_itinerary",
    "world_cities",
]
ext = ".json"


def insert_data(cursor, columns, data, table_name):
    """Insert data into the PostgreSQL table."""
    insert_query = """
    INSERT INTO {} ({}) VALUES ({});
    """.format(
        table_name, ", ".join(map(str, columns)), ", ".join(["%s" for _ in columns])
    )
    cursor.executemany(insert_query, data)


def read_json(file_path):
    """Read JSON data from file."""
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def main():
    """Seed the PostgreSQL database with data from JSON files."""
    # Connect to PostgreSQL
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    for table_name in table_names:
        full_path = json_file_path + table_name + ext
        # Read data from the JSON file
        json_data = read_json(full_path)

        # Get the column names from the keys of the first element in the JSON data
        columns = list(json_data[0].keys())

        # Insert data into the PostgreSQL table
        insert_data(cursor, columns, [list(d.values()) for d in json_data], table_name)

        connection.commit()

    connection.close()


if __name__ == "__main__":
    main()
